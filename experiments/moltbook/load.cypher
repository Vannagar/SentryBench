// Load the exported Moltbook influence graph. Run via neo4j.sh load.
CREATE CONSTRAINT event_id IF NOT EXISTS FOR (e:Event) REQUIRE e.id IS UNIQUE;
CREATE CONSTRAINT agent_id IF NOT EXISTS FOR (a:Agent) REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT submolt_name IF NOT EXISTS FOR (s:Submolt) REQUIRE s.name IS UNIQUE;

LOAD CSV WITH HEADERS FROM 'file:///events.csv' AS r
CALL (r) {
  CREATE (:Event {id: r.id, kind: r.kind, thread: r.thread, time: datetime(r.time),
                  submolt: r.submolt, flagged: r.flagged = 'True', position: toInteger(r.position), text: r.text})
} IN TRANSACTIONS OF 5000 ROWS;

LOAD CSV WITH HEADERS FROM 'file:///agents.csv' AS r
CALL (r) { CREATE (:Agent {id: r.id, name: r.name}) } IN TRANSACTIONS OF 5000 ROWS;

LOAD CSV WITH HEADERS FROM 'file:///submolts.csv' AS r
CREATE (:Submolt {name: r.name});

LOAD CSV WITH HEADERS FROM 'file:///influences.csv' AS r
CALL (r) {
  MATCH (a:Event {id: r.src}), (b:Event {id: r.dst})
  CREATE (a)-[:INFLUENCES {weight: toFloat(r.weight)}]->(b)
} IN TRANSACTIONS OF 5000 ROWS;

LOAD CSV WITH HEADERS FROM 'file:///replies.csv' AS r
CALL (r) {
  MATCH (a:Event {id: r.src}), (b:Event {id: r.dst})
  CREATE (a)-[:REPLIES_TO]->(b)
} IN TRANSACTIONS OF 5000 ROWS;

LOAD CSV WITH HEADERS FROM 'file:///authored.csv' AS r
CALL (r) {
  MATCH (a:Agent {id: r.agent}), (e:Event {id: r.event})
  CREATE (a)-[:AUTHORED]->(e)
} IN TRANSACTIONS OF 5000 ROWS;

MATCH (e:Event) WHERE e.submolt <> ''
MATCH (s:Submolt {name: e.submolt})
CALL (e, s) { CREATE (e)-[:IN]->(s) } IN TRANSACTIONS OF 5000 ROWS;
