---
name: ddia-principles
description: >
  Designing Data-Intensive Applications (DDIA) distilled reference guide by Martin Kleppmann.
  MUST be loaded when: designing database schemas, choosing storage engines, implementing replication
  or partitioning, handling distributed transactions, building batch/stream processing pipelines,
  choosing consistency models, implementing consensus, designing data flow architectures,
  evaluating trade-offs between availability and consistency, encoding/serialization decisions,
  data modeling (relational vs document vs graph), building fault-tolerant systems, or any
  system design and architecture discussion involving data-intensive applications.
  Trigger on: database design, replication, partitioning, sharding, transactions, isolation levels,
  consistency, consensus, CAP theorem, batch processing, stream processing, MapReduce, Kafka,
  event sourcing, CDC, OLTP, OLAP, B-tree, LSM-tree, data warehouse, schema evolution,
  encoding formats, distributed systems, fault tolerance, leader election, quorum.
---

# Designing Data-Intensive Applications — Distilled Guide

> Source: Martin Kleppmann, *Designing Data-Intensive Applications*
> Central thesis: **Data is the core challenge of modern applications — not compute.**

---

## Part I: Foundations of Data Systems

### Chapter 1: Reliability, Scalability, Maintainability

#### Three Pillars

| Pillar | Definition | Key Metric |
|--------|-----------|------------|
| **Reliability** | System works correctly even when faults occur | Fault ≠ Failure; tolerate faults, prevent failures |
| **Scalability** | System handles load growth gracefully | Measure with percentiles: p50, p95, p99, p999 |
| **Maintainability** | System is easy to operate, understand, evolve | Operability + Simplicity + Evolvability |

#### Fault Categories
- **Hardware**: Random, independent (disk, RAM, power). Mitigate with redundancy (RAID, dual power).
- **Software**: Systematic bugs affecting all nodes simultaneously (leap-second bug). Mitigate with process isolation, monitoring, chaos engineering.
- **Human**: #1 cause of outages (config errors). Mitigate with good abstractions, sandboxes, canary deployments, fast rollback.

#### Scalability Patterns
- **Vertical (scale-up)**: Bigger machine. Simple but has ceiling.
- **Horizontal (scale-out)**: More machines (shared-nothing). Complex but unlimited.
- **Elastic**: Auto-scale on load detection. Good for unpredictable workloads.

**Twitter fan-out case study**: 4.6k writes/s but 300k reads/s. Solution: pre-compute timelines (write fan-out) for most users; read-time merge for celebrities.

#### Performance: Use Percentiles, Not Averages
- p50 = median. p99 = tail latency matters for user experience.
- Amazon: 100ms delay = 1% revenue loss.
- **Tail latency amplification**: One slow backend call slows entire parallel request.

---

### Chapter 2: Data Models & Query Languages

#### Model Selection Guide

| Model | Best For | Weakness |
|-------|----------|----------|
| **Relational** | Structured data, complex joins, ACID transactions | Rigid schema, impedance mismatch with OOP |
| **Document** | Hierarchical data, flexible schema, data locality | Poor joins, many-to-many relationships |
| **Graph** | Highly connected data, variable-depth traversals | Less mature tooling, harder to partition |

#### Schema Strategy
- **Schema-on-write** (relational): Enforce structure at write time. Early error detection, migration cost.
- **Schema-on-read** (document): Interpret structure at read time. Flexible but validation burden on app.

#### Normalization vs Denormalization
- **Normalize**: Single source of truth, consistent updates, requires joins.
- **Denormalize**: Faster reads, risks inconsistency, update anomalies.

**Trend**: Models converge — PostgreSQL supports JSON, MongoDB added joins. Choose based on access patterns, not ideology.

---

### Chapter 3: Storage & Retrieval

#### Storage Engine Comparison

| Feature | B-Tree | LSM-Tree |
|---------|--------|----------|
| Write throughput | Lower (in-place update + WAL) | Higher (sequential append) |
| Read latency | More predictable | May check multiple SSTables |
| Write amplification | Higher | Lower |
| Space efficiency | Fragmentation possible | Better compression |
| Transaction support | Simpler (lock on tree node) | More complex |
| Used by | PostgreSQL, MySQL, Oracle | LevelDB, RocksDB, Cassandra |

#### OLTP vs OLAP

| Aspect | OLTP | OLAP |
|--------|------|------|
| Access | Random, few records | Sequential scan, millions of rows |
| Users | End users | Analysts |
| Data | Current state | Historical events |
| Scale | GB–TB | TB–PB |
| Optimize for | Low latency | Throughput |

#### Data Warehousing
- **ETL**: Extract from OLTP → Transform → Load into warehouse.
- **Star schema**: Central fact table (events) + dimension tables (attributes). Fact tables can have 100+ columns and petabyte scale.
- **Column-oriented storage**: Store each column separately. Huge I/O savings when queries touch few columns. Enables bitmap encoding, run-length compression, vectorized processing.

---

### Chapter 4: Encoding & Evolution

#### Format Comparison

| Format | Size (example) | Schema | Evolution | Cross-language |
|--------|---------------|--------|-----------|----------------|
| JSON | 81 bytes | Implicit | Manual | Excellent |
| Thrift | 59 bytes | Required | Field tags | Good |
| Protobuf | 33 bytes | Required | Field tags | Excellent |
| Avro | 32 bytes | Required | Name matching | Good |

#### Compatibility Rules
- **Backward compatible**: New code reads old data. *(Always required)*
- **Forward compatible**: Old code reads new data. *(Required for rolling upgrades)*
- Rule: Only add/remove fields with default values. Never reuse deleted field tags.

#### Data Flow Patterns
1. **Via databases**: Multiple code versions coexist during rolling deploys. Data outlives code.
2. **Via services (REST/RPC)**: Servers update before clients. Backward compat on requests, forward compat on responses.
3. **Via async messaging**: Decouples producers/consumers. Supports independent version evolution.

**Avoid**: Language-specific serialization (Java Serializable, Python pickle) — vendor lock-in + security risk.

---

## Part II: Distributed Data

### Chapter 5: Replication

#### Replication Models

| Model | Writes | Conflict | Use Case |
|-------|--------|----------|----------|
| **Single-leader** | One node | None | Most common (PostgreSQL, MySQL) |
| **Multi-leader** | Multiple nodes | Must resolve | Multi-datacenter, offline clients |
| **Leaderless** | Any node | Must resolve | Cassandra, Riak, Voldemort |

#### Sync vs Async Replication
- **Sync**: Durable, blocks on replica failure.
- **Async**: Fast, risks data loss on leader failure.
- **Semi-sync**: One replica sync, rest async. Practical compromise.

#### Replication Lag Problems & Solutions

| Problem | Symptom | Solution |
|---------|---------|----------|
| **Read-after-write** | User doesn't see own write | Read from leader for user's own data |
| **Monotonic reads** | Data goes backward in time | Stick user to one replica |
| **Consistent prefix reads** | Causal order violated | Write causally related data to same partition |

#### Conflict Resolution
- **Last-Write-Wins (LWW)**: Simple but loses data. Only safe if keys are immutable.
- **Merge**: Union values, concatenate, CRDT data structures.
- **Application-level**: Return all versions ("siblings"), let app decide.
- **Version vectors**: Track causal dependencies per replica.

#### Quorum: `w + r > n`
- w = write acknowledgments, r = read queries, n = total replicas.
- **Sloppy quorum**: Accept writes on non-home nodes during partitions (hinted handoff). Improves availability, weakens consistency.

---

### Chapter 6: Partitioning (Sharding)

#### Partitioning Strategies

| Strategy | Pros | Cons |
|----------|------|------|
| **Key-range** | Efficient range queries | Hotspot risk on sequential keys |
| **Hash** | Even distribution | No range queries |
| **Compound** | First part hashed, rest sorted | More complex, best of both |

#### Secondary Index Partitioning
- **Local (document-based)**: Each partition indexes its own data. Writes simple, reads scatter-gather.
- **Global (term-based)**: Index partitioned by term. Reads efficient, writes update multiple partitions.

#### Rebalancing
- **Fixed partition count**: More partitions than nodes. Redistribute on node changes. (Riak, Elasticsearch)
- **Dynamic**: Split/merge based on size. (HBase, RethinkDB)
- **Proportional to nodes**: Fixed partitions per node. (Cassandra)

#### Request Routing
- Round-robin to any node (node forwards if needed)
- Routing layer (partition-aware proxy)
- Client-aware (client knows partition map)
- **ZooKeeper**: Authoritative partition → node mapping. Used by HBase, Kafka.

---

### Chapter 7: Transactions

#### Isolation Levels (Weakest → Strongest)

| Level | Prevents | Allows | Implementation |
|-------|----------|--------|----------------|
| **Read Committed** | Dirty reads, dirty writes | Non-repeatable reads, lost updates | Row locks + old value copy |
| **Snapshot Isolation** | + Non-repeatable reads | Write skew, phantoms | MVCC (multi-version) |
| **Serializable** | Everything | Nothing | 2PL, serial execution, or SSI |

#### Concurrency Anomalies

| Anomaly | Description | Example |
|---------|-------------|---------|
| **Dirty read** | See uncommitted data | Reading half-written transfer |
| **Dirty write** | Overwrite uncommitted data | Two buyers "winning" same item |
| **Lost update** | Read-modify-write race | Two concurrent counter increments |
| **Write skew** | Decision based on stale read | Two doctors both going off-call |
| **Phantom** | New rows change query result | Meeting room double-booking |

#### Serializable Implementations
1. **Serial execution**: Single thread, in-memory. Fast but limited throughput. (VoltDB, Redis)
2. **Two-Phase Locking (2PL)**: Shared/exclusive locks held until commit. Strong but slow, deadlock-prone.
3. **SSI (Serializable Snapshot Isolation)**: Optimistic — execute freely, detect conflicts at commit. Best performance for read-heavy workloads. (PostgreSQL 9.1+)

---

### Chapter 8: Troubles with Distributed Systems

#### The Three Unreliabilities

**Networks**: Async packet networks — no delivery guarantee, no timing guarantee. Cannot distinguish crash from network delay. Timeouts are the only failure detector, but no correct timeout value exists.

**Clocks**:
- Wall clocks: Can jump backward (NTP correction). Never use for ordering events.
- Monotonic clocks: Safe for elapsed time, not cross-node comparison.
- Quartz drift: ~200ppm → 6ms error every 30 seconds.

**Processes**: GC pauses, VM suspension, page faults — threads stop without warning. A paused node doesn't know time passed.

#### Key Principles
- **Fault ≠ failure**: Design for partial failures. Some nodes work while others don't.
- **Truth is defined by majority**: Individual nodes cannot determine system state alone. Quorum votes decide.
- **Fencing tokens**: Monotonically increasing tokens prevent zombie processes from corrupting state.
- **Safety vs liveness**: Safety (bad things never happen) must hold always. Liveness (good things eventually happen) may have conditions.

---

### Chapter 9: Consistency & Consensus

#### Consistency Models (Strongest → Weakest)

| Model | Guarantee | Cost |
|-------|-----------|------|
| **Linearizability** | Behaves as if one copy, all ops atomic | High latency, reduced availability during partition |
| **Causal consistency** | Respects cause-effect ordering | Better performance, partition-tolerant |
| **Eventual consistency** | Replicas converge eventually | Best performance, weakest guarantee |

#### Linearizability Use Cases
- Leader election / distributed locks
- Uniqueness constraints (usernames, filenames)
- Cross-channel coordination (message queue + storage)

#### Consensus Algorithms
- **2PC**: Coordinator-based, blocking on coordinator failure. Practical but fragile.
- **Paxos/Raft/Zab**: Epoch-based leader election + quorum voting. Non-blocking. Used by etcd, ZooKeeper, Consul.
- **FLP impossibility**: Consensus impossible in pure async systems with crashes. Practical algorithms use timeouts.

#### Total Order Broadcast ≡ Consensus ≡ Linearizable CAS
These three problems are mathematically equivalent. Solving one solves all.

#### ZooKeeper / etcd Pattern
- Small consensus cluster (3–5 nodes) for coordination.
- Linearizable atomic CAS operations.
- Failure detection via session heartbeats.
- Applications: leader election, partition assignment, distributed locks, service discovery.

---

## Part III: Derived Data

### Chapter 10: Batch Processing

#### Unix Philosophy → MapReduce
- Each program does one thing well.
- Output of one program = input of another.
- Immutable inputs, deterministic processing.

#### MapReduce Pipeline
`Input → Mapper (extract key-value) → Sort/Partition → Reducer (aggregate by key) → Output`

#### Distributed Join Strategies

| Join Type | When | How |
|-----------|------|-----|
| **Sort-merge** | Both inputs large | Sort by join key, merge in reducer |
| **Broadcast hash** | One input small (fits in RAM) | Load small side as hash table |
| **Partitioned hash** | Both inputs partitioned identically | Per-partition hash join |

#### Beyond MapReduce: Dataflow Engines (Spark, Flink, Tez)
- Treat entire workflow as single job.
- Pipeline intermediate results (avoid full materialization to HDFS).
- Keep data in memory where possible.
- Track computation lineage for fault recovery (RDDs).
- Support iterative algorithms (graph processing via Pregel/BSP model).

---

### Chapter 11: Stream Processing

#### Message Broker Models

| Model | Delivery | Ordering | Replay | Use Case |
|-------|----------|----------|--------|----------|
| **AMQP/JMS** | Per-message ack, delete after | No ordering guarantee | No | Task queues, async RPC |
| **Log-based (Kafka)** | Offset-based, retained | Per-partition ordering | Yes | Event streaming, CDC |

#### Change Data Capture (CDC)
Extract database changes as event stream → keep derived systems (search indexes, caches, warehouses) in sync. **Source of truth stays in database; derived views are consumers.**

#### Event Sourcing
Model state as append-only sequence of business events (not DB operations). Events are immutable facts. Current state = fold over event history.

#### Stream Joins

| Join | Input A | Input B | State |
|------|---------|---------|-------|
| **Stream-Stream** | Events | Events | Time-windowed buffer |
| **Stream-Table** | Events | DB snapshot (via CDC) | Local materialized table |
| **Table-Table** | CDC stream | CDC stream | Derived materialized view |

#### Time & Windowing

| Window | Description |
|--------|-------------|
| **Tumbling** | Fixed-size, non-overlapping (e.g., every 1 min) |
| **Hopping** | Fixed-size, overlapping (e.g., 1 min window every 30s) |
| **Sliding** | All events within time threshold of each other |
| **Session** | Grouped by activity gap (e.g., 30 min inactivity) |

**Event time ≠ processing time.** Always use event time for correctness. Handle late events with watermarks or correction publishes.

#### Processing Guarantees
- **Microbatching** (Spark Streaming): ~1s latency, atomic small batches.
- **Checkpointing** (Flink): Periodic snapshots with message barriers.
- **Idempotency**: Deduplicate using message offsets or unique IDs.
- End-to-end exactly-once requires idempotent output + deduplication.

---

### Chapter 12: The Future of Data Systems

#### Data Integration Pattern
No single database does everything. Use **event log as integration backbone**:
1. All writes go through authoritative event log.
2. Derived systems (indexes, caches, ML models) consume the log.
3. Deterministic, idempotent functions transform between layers.

#### Unbundling Databases
Separate concerns:
- **Record system**: Captures authoritative writes.
- **Derived systems**: Indexes, caches, materialized views consume change streams.
- Enables gradual migration — run old and new systems in parallel.

#### End-to-End Exactly-Once
Low-level guarantees (TCP, DB transactions) don't ensure application correctness. Require:
- **Operation identifiers**: UUID-based deduplication at application level.
- **Idempotent operations**: Same effect whether executed once or many times.
- **Unique constraint enforcement**: Via partitioned stream processing.

#### Async Constraint Enforcement
Instead of distributed transactions:
1. Route requests by constraint field to partitioned log.
2. Stream processor sequences competing requests.
3. Reject violations, notify clients via output stream.
4. Some applications tolerate temporary violations with compensating transactions.

#### Auditability
- Treat data like immutable event log — enables reconstruction and verification.
- Implement cryptographic audit trails (Merkle trees).
- Periodically test backup restoration and data reconstruction.

---

## Decision Framework: Quick Reference

### Choosing a Data Model
```
Many-to-many relationships?     → Relational or Graph
Hierarchical / nested data?     → Document
Highly connected data?          → Graph
Flexible / evolving schema?     → Document (schema-on-read)
Strong consistency required?    → Relational (ACID)
```

### Choosing a Storage Engine
```
Write-heavy workload?           → LSM-tree (RocksDB, Cassandra)
Read-heavy, predictable?        → B-tree (PostgreSQL, MySQL)
Analytical queries?             → Column store (ClickHouse, Redshift)
Full-text search?               → Inverted index (Elasticsearch)
```

### Choosing a Replication Strategy
```
Single datacenter?              → Single-leader
Multi-datacenter?               → Multi-leader
Offline-first clients?          → Multi-leader or Leaderless
Maximum availability?           → Leaderless with sloppy quorum
Strong consistency?             → Single-leader with sync replication
```

### Choosing an Isolation Level
```
Read-only analytics?            → Snapshot isolation
General OLTP?                   → Read committed (default in most DBs)
Financial / critical?           → Serializable (prefer SSI over 2PL)
High write contention?          → Serial execution (if data fits in RAM)
```

### Choosing Batch vs Stream
```
Historical data reprocessing?   → Batch (Spark, Flink batch mode)
Real-time derived views?        → Stream (Kafka + Flink/Spark Streaming)
Both needed?                    → Unified engine (Flink) over Lambda architecture
```
