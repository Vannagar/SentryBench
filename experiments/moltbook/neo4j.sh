#!/usr/bin/env bash
# Local Neo4j for the Moltbook influence graph. Run from the repo root.
#   bash experiments/moltbook/neo4j.sh start   # start Neo4j (browser at http://localhost:7474)
#   bash experiments/moltbook/neo4j.sh load    # export CSVs and load them (wipes the graph first)
#   bash experiments/moltbook/neo4j.sh stop    # stop and remove the container (data is kept)
# Login: neo4j / sentrybench   (local only, bound to 127.0.0.1)
set -euo pipefail
NAME=sentrybench-neo4j
ROOT="$(pwd)/data/neo4j"
AUTH=neo4j/sentrybench

case "${1:-}" in
  start)
    mkdir -p "$ROOT/data" "$ROOT/import"
    if [ "$(docker ps -q -f name=^${NAME}$)" ]; then
      echo "Already running: http://localhost:7474  (neo4j / sentrybench)"; exit 0
    elif [ "$(docker ps -aq -f name=^${NAME}$)" ]; then
      docker start "$NAME" >/dev/null
    else
    docker run -d --name "$NAME" --user "$(id -u):$(id -g)" \
      -p 127.0.0.1:7474:7474 -p 127.0.0.1:7687:7687 \
      -v "$ROOT/data:/data" -v "$ROOT/import:/import" \
      -e NEO4J_AUTH="$AUTH" \
      -e NEO4J_server_memory_heap_max__size=2G \
      neo4j:5-community
    fi
    echo "Waiting for Neo4j..."
    until docker exec "$NAME" cypher-shell -u neo4j -p sentrybench "RETURN 1" >/dev/null 2>&1; do sleep 2; done
    echo "Ready: http://localhost:7474  (neo4j / sentrybench)"
    ;;
  load)
    python3 experiments/moltbook/export_neo4j.py
    echo "Clearing old graph..."
    docker exec "$NAME" cypher-shell -u neo4j -p sentrybench \
      "MATCH (n) CALL (n) { DETACH DELETE n } IN TRANSACTIONS OF 10000 ROWS"
    echo "Loading (takes a minute or two)..."
    docker exec -i "$NAME" cypher-shell -u neo4j -p sentrybench < experiments/moltbook/load.cypher
    docker exec "$NAME" cypher-shell -u neo4j -p sentrybench \
      "MATCH (n) RETURN labels(n)[0] AS label, count(*) AS n ORDER BY n DESC"
    ;;
  stop)
    docker rm -f "$NAME"
    ;;
  *)
    echo "usage: $0 start|load|stop"; exit 1 ;;
esac
