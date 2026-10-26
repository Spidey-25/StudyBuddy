"""Extra authored questions that rotate through platform-game sessions."""

ROTATING_LEVELS = {
    "cpp-debugger": [
        {"prompt":"int product(int a, int b) { return a + b; }", "task":"Return the product of both arguments.", "answer":"return a * b;", "tests":["product(3, 4) is 12", "product(-2, 5) is -10"], "hint":"The function needs multiplication, not addition."},
        {"prompt":"int positive = 0; for (int value : values) { if (value > 0) positive = value; }", "task":"Count positive values rather than replacing the count.", "answer":"++positive;", "tests":["positive values [2, 5] give 2", "empty input gives 0"], "hint":"Each qualifying value contributes one to the count."},
    ],
    "cpp-output": [
        {"prompt":"int x = 5; cout << x++ + 2 << ' ' << x;", "answer":"7 6", "hint":"Post-increment supplies the old value to the expression.", "explanation":"The expression uses 5 + 2, then x has value 6."},
        {"prompt":"int a = 9, b = 4; cout << a % b << ' ' << a / b;", "answer":"1 2", "hint":"Both operators use integer arithmetic.", "explanation":"9 divided by 4 has quotient 2 and remainder 1."},
    ],
    "java-debugger": [
        {"prompt":"static boolean isEven(int number) { return number % 2 == 1; }", "task":"Return true only for even integers.", "answer":"return number % 2 == 0;", "tests":["isEven(8) is true", "isEven(3) is false", "isEven(0) is true"], "hint":"An even number has remainder zero when divided by two."},
        {"prompt":"static int smaller(int a, int b) { return a > b ? a : b; }", "task":"Return the smaller argument.", "answer":"return Math.min(a, b);", "tests":["smaller(2, 7) is 2", "smaller(-3, 0) is -3"], "hint":"Use the standard minimum operation."},
    ],
    "java-oop": [
        {"prompt":"A notification service must send email and SMS messages through one shared send operation.", "choices":["Define a notifier interface and implement it for email and SMS", "Put message delivery in a public static field", "Duplicate the whole service for each channel"], "answer":0, "hint":"The service should depend on a behavior contract.", "explanation":"A shared interface lets the service work with different delivery implementations."},
        {"prompt":"A shopping cart must calculate totals differently when a discount policy changes.", "choices":["Inject a pricing strategy behind a common interface", "Add unrelated global flags to the cart", "Make every cart field public"], "answer":0, "hint":"Keep the cart stable while swapping one focused behavior.", "explanation":"A strategy interface separates pricing rules from cart state."},
    ],
    "python-debug": [
        {"prompt":"def last_or_none(items):\n    return items[len(items)]", "task":"Return the last item, or None for an empty list.", "answer":"return items[-1] if items else None", "tests":["[4, 9] returns 9", "[] returns None"], "hint":"Check for an empty sequence and use its final valid position."},
        {"prompt":"def count_matches(values, target):\n    count = 0\n    for value in values:\n        if value == target:\n            count = value\n    return count", "task":"Increment the match count for each equal value.", "answer":"count += 1", "tests":["[2, 2, 3] with target 2 returns 2", "[] returns 0"], "hint":"Each match adds one; do not replace the count with the matched value."},
    ],
    "python-logic": [
        {"prompt":"Accept an index only when it is non-negative and smaller than the collection length.", "blocks":["0 <= index", "and", "index < len(items)"], "answer":["0 <= index", "and", "index < len(items)"], "hint":"The first valid index is zero and the upper bound is exclusive.", "explanation":"Both comparisons keep the index within the collection."},
        {"prompt":"Allow a retry when attempts remain and the service is available.", "blocks":["attempts < limit", "and", "service_available"], "answer":["attempts < limit", "and", "service_available"], "hint":"Both conditions must be true before a retry.", "explanation":"The conjunction respects the retry cap and service state."},
    ],
    "dsa-arena": [
        {"prompt":"Partition-based quicksort on an unsorted range", "steps":["Choose a pivot", "Move smaller values before the pivot", "Place the pivot in its final position", "Recursively sort the two remaining ranges"], "hint":"Partition establishes the pivot's final position before recursive work.", "explanation":"Quicksort recursively sorts the partitions around the pivot."},
        {"prompt":"Topological ordering of a directed acyclic graph", "steps":["Count each node's incoming edges", "Queue nodes with zero incoming edges", "Remove one queued node and append it to the order", "Reduce incoming counts of its neighbours and queue new zeros"], "hint":"Start with nodes that have no unmet prerequisites.", "explanation":"Kahn's algorithm repeatedly removes zero-indegree nodes."},
    ],
    "dsa-visualizer": [
        {"prompt":"Start with an empty stack. Apply push(5), push(1), push(7), pop(), pop(). Enter bottom-to-top contents.", "operations":["push(5)","push(1)","push(7)","pop()","pop()"], "answer":[5], "structure":"Stack", "hint":"Each pop removes the most recently pushed item.", "explanation":"7 and then 1 are removed, leaving 5."},
        {"prompt":"Start with an empty queue. Enqueue M, N, P; dequeue; enqueue Q; dequeue. Enter front-to-back contents.", "operations":["enqueue(M)","enqueue(N)","enqueue(P)","dequeue()","enqueue(Q)","dequeue()"], "answer":["P","Q"], "structure":"Queue", "hint":"A queue removes the oldest item first.", "explanation":"M and N leave first; P stays ahead of Q."},
    ],
    "dbms-sql": [
        {"prompt":"Table Orders(id, customer_id, total). Return orders above 100, highest total first.", "answer":"SELECT id, customer_id, total FROM Orders WHERE total > 100 ORDER BY total DESC;", "hint":"Filter totals, then sort descending.", "explanation":"WHERE selects qualifying rows and ORDER BY ranks them."},
        {"prompt":"Table Tickets(id, status, created_at). Count tickets per status, largest count first.", "answer":"SELECT status, COUNT(*) FROM Tickets GROUP BY status ORDER BY COUNT(*) DESC;", "hint":"Group by the status and aggregate each group.", "explanation":"COUNT and GROUP BY produce one total per status."},
    ],
    "dbms-er": [
        {"prompt":"A patient can have many appointments; each appointment belongs to one patient.", "choices":["Patient 1:N Appointment", "Patient M:N Appointment", "Patient 1:1 Appointment"], "answer":0, "hint":"One patient can appear in many appointment records.", "explanation":"Patient is the one side and Appointment is the many side."},
        {"prompt":"An author can write many books and a book can have multiple co-authors.", "choices":["Author M:N Book, resolved with BookAuthor", "Author 1:1 Book", "Author 1:N Book only"], "answer":0, "hint":"Both sides can participate in multiple relationships.", "explanation":"A junction entity records the many-to-many association."},
    ],
    "os-scheduler": [
        {"prompt":"Non-preemptive SJF. Burst times: T1=5, T2=1, T3=6, T4=3.", "jobs":["T1 (5)","T2 (1)","T3 (6)","T4 (3)"], "answer":["T2","T4","T1","T3"], "hint":"Order the available jobs by increasing burst time.", "explanation":"The shortest-to-longest order is 1, 3, 5, 6."},
        {"prompt":"Non-preemptive SJF. Burst times: A=4, B=2, C=7, D=1.", "jobs":["A (4)","B (2)","C (7)","D (1)"], "answer":["D","B","A","C"], "hint":"Choose the smallest burst first, then the next smallest.", "explanation":"SJF orders these jobs by burst time 1, 2, 4, 7."},
    ],
    "os-memory": [
        {"prompt":"Blocks [180, 420, 260]. Requests [150, 240, 100]. Enter first-fit block indexes (0-based).", "blocks":[180,420,260], "requests":[150,240,100], "answer":[0,1,0], "hint":"Reduce the chosen block's remaining capacity after every request.", "explanation":"The remaining blocks lead first-fit to choose 0, then 1, then 0."},
        {"prompt":"Blocks [90, 310, 500]. Requests [250, 85, 220]. Enter first-fit block indexes (0-based).", "blocks":[90,310,500], "requests":[250,85,220], "answer":[1,0,2], "hint":"Scan from block zero for each request using updated free sizes.", "explanation":"The requests fit first in block 1, then 0, then 2."},
    ],
    "cn-routing": [
        {"prompt":"Route K to R using the fewest hops. Links: K-L, L-R, K-M, M-N, N-R, L-N.", "nodes":["K","L","M","N","R"], "edges":[["K","L"],["L","R"],["K","M"],["M","N"],["N","R"],["L","N"]], "start":"K", "end":"R", "answer":["K","L","R"], "hint":"Choose a valid path with the fewest links.", "explanation":"K-L-R reaches R in two hops."},
        {"prompt":"Route Hub to API. Links: Hub-Edge, Edge-Cache, Cache-API, Hub-Core, Core-API, Edge-Core.", "nodes":["Hub","Edge","Cache","API","Core"], "edges":[["Hub","Edge"],["Edge","Cache"],["Cache","API"],["Hub","Core"],["Core","API"],["Edge","Core"]], "start":"Hub", "end":"API", "answer":["Hub","Core","API"], "hint":"Compare the short Core path with the Cache path.", "explanation":"Hub-Core-API uses two links."},
    ],
    "cn-troubleshoot": [
        {"prompt":"A laptop has a valid IP and gateway, but cannot reach its local DNS resolver. What should you check first?", "choices":["VLAN, local route, or firewall reachability to the resolver", "The remote website's CSS", "Browser bookmarks", "The monitor cable"], "answer":0, "hint":"The failure is before name resolution can complete.", "explanation":"Check local network reachability and filtering to the configured resolver."},
        {"prompt":"A site resolves to an IP, but TLS reports that the certificate name does not match.", "choices":["Verify the hostname, certificate, and reverse-proxy configuration", "Flush the keyboard buffer", "Change the subnet mask randomly", "Disable certificate validation"], "answer":0, "hint":"DNS succeeded; the identity presented by TLS is inconsistent.", "explanation":"The hostname and certificate chain need to match; disabling validation is unsafe."},
    ],
    "web-playground": [
        {"prompt":"<p id=\"status\"></p>\n<!-- Add a safe text-only update -->", "task":"Set the paragraph text without parsing user input as HTML.", "answer":"status.textContent = message;", "tests":["assigns textContent", "does not parse a string as HTML"], "hint":"Use the DOM property intended for plain text.", "difficulty":"Hard"},
        {"prompt":".panel {\n  /* Center content in both directions with CSS Grid */\n}", "task":"Use a grid declaration to center the panel contents.", "answer":"display: grid; place-items: center;", "tests":["grid layout is enabled", "items are centered on both axes"], "hint":"Enable Grid and use its two-axis alignment shorthand.", "difficulty":"Hard"},
    ],
    "web-ui-debug": [
        {"prompt":"A form field has no visible label and its placeholder disappears while typing.", "choices":["Add a persistent label associated with the field's id", "Use placeholder text as the only label", "Hide the field name from assistive technology"], "answer":0, "hint":"The field needs a name that remains visible and programmatically associated.", "explanation":"A real label stays available and exposes the field's accessible name."},
        {"prompt":"A status message appears after saving, but screen readers are not told that it changed.", "choices":["Use a polite live region for the status message", "Move focus to the page title after every save", "Make the message an unlabelled image"], "answer":0, "hint":"Announce dynamic status without unexpectedly moving focus.", "explanation":"A polite live region communicates updates while preserving the user's current focus."},
    ],
    "c-debugger": [
        {"prompt":"int last_value(int values[], int count) { return values[count]; }", "task":"Return the last element of a non-empty array.", "answer":"return values[count - 1];", "tests":["count 1 returns index 0", "count 4 returns index 3"], "hint":"The number of elements is one greater than the final valid index."},
        {"prompt":"int magnitude(int value) { return value; }", "task":"Return the non-negative magnitude of value.", "answer":"return value < 0 ? -value : value;", "tests":["-8 becomes 8", "5 remains 5"], "hint":"Negate only values below zero."},
    ],
    "c-memory-trace": [
        {"prompt":"int values[] = {8, 3, 6}; int *p = values; printf(\"%d\", *p + *(p + 2));", "answer":"14", "hint":"Dereference the first and third elements, then add them.", "explanation":"8 + 6 prints 14."},
        {"prompt":"int values[] = {5, 10, 15, 20}; int *p = &values[1]; printf(\"%d\", *(p + 2));", "answer":"20", "hint":"Pointer arithmetic advances by elements from index one.", "explanation":"p+2 points to values[3], which contains 20."},
    ],
    "se-requirements": [
        {"prompt":"A team must ship a reporting feature that depends on a stable data contract.", "steps":["Identify report users and decisions", "Agree on the data contract", "Write measurable acceptance criteria", "Implement and verify the report"], "hint":"Clarify the consumer and contract before building the feature.", "explanation":"The report can be verified only after its users, data and acceptance rules are clear."},
        {"prompt":"A release needs a rollback path before a database change is deployed.", "steps":["Document compatibility and rollback requirements", "Prepare a reversible migration", "Test migration and rollback on a copy", "Deploy gradually and monitor"], "hint":"Prove recovery before applying the change to production.", "explanation":"A tested reversible migration reduces the risk of an unsafe release."},
    ],
    "se-test-design": [
        {"prompt":"A password must contain 8 to 64 characters. Which cases best cover boundaries?", "choices":["7, 8, 64, and 65 characters", "20 and 30 characters only", "One password of length 32"], "answer":0, "hint":"Test immediately outside and exactly at both limits.", "explanation":"These values cover both valid edges and adjacent invalid inputs."},
        {"prompt":"A transfer must reject insufficient funds and preserve the balance. Which test is strongest?", "choices":["Check a successful transfer and verify a rejected transfer leaves the balance unchanged", "Check only that the button is blue", "Run the transfer once with an unlimited balance"], "answer":0, "hint":"Test the invariant before and after the failure path.", "explanation":"The balance invariant must hold even when the operation is rejected."},
    ],
    "ai-inference": [
        {"prompt":"Facts: has_key(ari), at_door(ari). Rule: has_key(X) AND at_door(X) → may_enter(X). What follows?", "answer":"may_enter(ari)", "hint":"Substitute ari into both premises.", "explanation":"Both facts match, so the rule derives may_enter(ari)."},
        {"prompt":"Facts: paid(order7), packed(order7). Rule: paid(X) AND packed(X) → ready_to_ship(X). What is inferred?", "answer":"ready_to_ship(order7)", "hint":"Both premises refer to the same order.", "explanation":"The rule fires for order7 because it is paid and packed."},
    ],
    "ai-feature-lab": [
        {"prompt":"A model predicts whether a customer will renew before the renewal date. Which feature is safe to use?", "choices":["Usage history available before the renewal date", "Whether the customer renewed later", "A cancellation reason recorded after the decision"], "answer":0, "hint":"A feature must exist at prediction time.", "explanation":"Later outcomes leak information unavailable when the prediction is made."},
        {"prompt":"A vision model must classify damaged parts under different lighting.", "choices":["Include representative lighting conditions in training and evaluation", "Train and test only on one lighting setup", "Use image filenames as the label"], "answer":0, "hint":"The examples should reflect conditions expected in use.", "explanation":"Representative evaluation helps reveal whether performance generalizes across lighting."},
    ],
    "ml-metric-match": [
        {"prompt":"A fraud review team has limited capacity and wants flagged transactions to be trustworthy.", "choices":["Precision at the review threshold", "Training accuracy only", "Number of hidden layers", "Total row count"], "answer":0, "hint":"The team cares about correctness among flagged positives.", "explanation":"Precision measures the share of flagged cases that are truly positive."},
        {"prompt":"A safety detector must catch nearly every hazardous event, even with some extra alerts.", "choices":["Recall, alongside the false-positive cost", "Specificity alone", "Training time", "Feature count"], "answer":0, "hint":"Missed positive events are the primary concern.", "explanation":"Recall measures how many actual positive events are detected."},
    ],
    "ml-overfit-lab": [
        {"prompt":"A model performs well on training data but poorly on a clean validation set.", "choices":["Reduce overfitting with regularization or simpler features", "Tune repeatedly on the final test set", "Add more parameters without checking data"], "answer":0, "hint":"The gap suggests memorization rather than generalization.", "explanation":"Regularization and feature review can improve performance on unseen data."},
        {"prompt":"Validation scores vary widely across random splits because one small group is rare.", "choices":["Use stratified or repeated evaluation and report uncertainty", "Choose the split with the highest score", "Hide the rare group from evaluation"], "answer":0, "hint":"The estimate is unstable, so measure variability carefully.", "explanation":"Repeated or stratified evaluation makes uncertainty and group coverage visible."},
    ],
    "cyber-incident": [
        {"prompt":"An exposed API token is found in a public repository.", "steps":["Record the discovery and preserve relevant evidence", "Revoke the exposed token", "Review its use and contain affected access", "Rotate dependent secrets and remove the exposure", "Monitor and document recovery"], "hint":"Stop the credential from working before relying on repository cleanup.", "explanation":"Revocation limits access; review and rotation address possible impact and related secrets."},
        {"prompt":"A server begins sending unusual outbound traffic after an alert.", "steps":["Confirm and record the alert", "Contain the host using the approved isolation process", "Preserve logs and determine scope", "Remove the cause and restore from a trusted state", "Monitor for recurrence"], "hint":"Contain the host while keeping evidence for investigation.", "explanation":"Isolation limits spread while evidence supports investigation and recovery."},
    ],
    "cyber-phishing": [
        {"prompt":"A message asks you to scan a QR code to keep your work account active.", "choices":["Verify through the known IT portal and report the message", "Scan it on a personal phone", "Reply with your one-time code"], "answer":0, "hint":"Use a known channel instead of a link supplied by the message.", "explanation":"Independent verification avoids entering credentials on an attacker-controlled page."},
        {"prompt":"A file-sharing notice asks you to sign in with your work password on an unfamiliar domain.", "choices":["Open the official service from a saved address and report the notice", "Enter the password to preview the file", "Forward the link to coworkers"], "answer":0, "hint":"Check the service through an address you already trust.", "explanation":"A familiar route avoids trusting the sender's destination."},
    ],
    "cloud-architecture": [
        {"prompt":"A web service must survive the loss of one application instance during a deployment.", "choices":["Run multiple stateless instances behind health checks", "Store the only user session in one process's memory", "Disable readiness checks"], "answer":0, "hint":"Requests should continue on healthy instances.", "explanation":"Stateless instances and health checks allow traffic to avoid failed nodes."},
        {"prompt":"A batch job should not run twice when a queue message is delivered again.", "choices":["Make job processing idempotent and track a stable job key", "Retry without a job identifier", "Delete the queue after each message"], "answer":0, "hint":"A repeated delivery needs to be recognized as the same work.", "explanation":"Idempotency keys prevent duplicate side effects after retries."},
    ],
    "cloud-cost": [
        {"prompt":"A job runs 12 hours at $0.18 per hour. Enter the compute cost in dollars.", "answer":2.16, "hint":"Multiply runtime by the hourly rate.", "explanation":"12 × $0.18 = $2.16."},
        {"prompt":"A service stores 600 GB at $0.025 per GB-month. Enter the monthly storage cost.", "answer":15, "hint":"Multiply stored capacity by the per-GB-month rate.", "explanation":"600 × $0.025 = $15."},
    ],
    "embedded-interrupt": [
        {"prompt":"A sensor data-ready interrupt occurs while the main loop is updating a display.", "steps":["Acknowledge the data-ready event", "Copy the sample into a bounded buffer", "Set a pending-work flag", "Return quickly and process the sample in the main loop"], "hint":"Capture the event in the handler and defer slow work.", "explanation":"Deferred processing keeps interrupt latency short."},
        {"prompt":"A watchdog timer fires because the main task stopped responding.", "steps":["Record the reset cause when the system restarts", "Initialize hardware to a safe state", "Inspect the last known task progress", "Recover or report the fault and resume safely"], "hint":"Preserve the failure reason before normal operation overwrites it.", "explanation":"Recording the reset cause helps diagnose the stall before safe recovery."},
    ],
    "embedded-pinmap": [
        {"prompt":"A thermistor is connected to a microcontroller that measures analog voltage.", "choices":["Connect it through a suitable divider to an ADC input", "Connect it to two output pins", "Drive it directly from a high-current motor pin"], "answer":0, "hint":"A changing resistance must become a voltage the ADC can measure.", "explanation":"A divider creates a measurable voltage while respecting the input range."},
        {"prompt":"A 12 V relay coil must be controlled by a 3.3 V microcontroller output.", "choices":["Use a rated transistor or driver and a flyback diode", "Connect the coil directly to the GPIO", "Set the GPIO to analog input"], "answer":0, "hint":"The coil current and inductive kick exceed a GPIO's direct capability.", "explanation":"A driver handles the coil current and a diode suppresses the voltage spike."},
    ],
    "iot-protocol": [
        {"prompt":"A battery sensor sends periodic telemetry to one broker, and several dashboards subscribe to it.", "choices":["Use authenticated publish/subscribe topics", "Let every dashboard poll the sensor directly without identity", "Broadcast credentials inside each payload"], "answer":0, "hint":"Many consumers need selective delivery from a constrained publisher.", "explanation":"Brokered topics decouple the sensor from subscribers and authentication protects access."},
        {"prompt":"A device may reconnect after hours offline and must report whether a reading is stale.", "choices":["Attach a timestamp and sequence number to each reading", "Send the value without identity or time", "Replace missing readings with zero"], "answer":0, "hint":"Consumers need freshness and ordering information.", "explanation":"Timestamps and sequence numbers help detect stale or duplicated telemetry."},
    ],
    "iot-topology": [
        {"prompt":"Route Thermostat to Cloud in the fewest hops. Links: Thermostat-Bridge, Bridge-Cloud, Thermostat-Phone, Phone-WiFi, WiFi-Cloud.", "nodes":["Thermostat","Bridge","Cloud","Phone","WiFi"], "edges":[["Thermostat","Bridge"],["Bridge","Cloud"],["Thermostat","Phone"],["Phone","WiFi"],["WiFi","Cloud"]], "start":"Thermostat", "end":"Cloud", "answer":["Thermostat","Bridge","Cloud"], "hint":"Compare the two-link bridge route with the longer WiFi route.", "explanation":"Thermostat-Bridge-Cloud uses two hops."},
        {"prompt":"Route Sensor to Dashboard. Links: Sensor-Gateway, Gateway-Broker, Broker-Dashboard, Sensor-LocalHub, LocalHub-Dashboard.", "nodes":["Sensor","Gateway","Broker","Dashboard","LocalHub"], "edges":[["Sensor","Gateway"],["Gateway","Broker"],["Broker","Dashboard"],["Sensor","LocalHub"],["LocalHub","Dashboard"]], "start":"Sensor", "end":"Dashboard", "answer":["Sensor","LocalHub","Dashboard"], "hint":"The LocalHub route is shorter than the broker route.", "explanation":"Sensor-LocalHub-Dashboard reaches the destination in two hops."},
    ],
}
