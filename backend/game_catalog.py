"""Deterministic, subject-specific educational mini-game catalog and rules."""
from __future__ import annotations

import ast
import math
import random
import re
import uuid
from .game_content import EXTRA_LEVELS, ROTATING_LEVELS
from . import code_checks


# Public game data is sanitized; private accepted actions remain server-side.
GAMES = {
    "cpp-debugger": {"subject":"CPP", "title":"C++ Code Debugger", "mechanic":"code-edit", "objective":"Repair a C++ statement and reason about its behavior.", "instructions":"Replace the faulty line. The server checks it against private, fixed exercise checks; it does not compile or execute submitted code.", "levels":[
        {"prompt":"int sum(int a, int b) { return a - b; }", "task":"Fix the return expression so sum adds its arguments.", "answer":"return a + b;", "tests":["sum(2, 3) == 5", "sum(-1, 1) == 0"], "hint":"The function should combine both arguments using addition."},
        {"prompt":"for (int i = 0; i <= values.size(); ++i) { use(values[i]); }", "task":"Fix the loop bound to avoid reading past the end.", "answer":"i < values.size()", "tests":["empty and non-empty vector bounds"], "hint":"The last valid index is size minus one."}]},
    "cpp-output": {"subject":"CPP", "title":"C++ Output & Logic Challenge", "mechanic":"output-predict", "objective":"Trace C++ expressions and predict their printed output.", "instructions":"Evaluate the expression using integer rules, then enter the output exactly.", "levels":[
        {"prompt":"int x = 7; cout << x / 2 << ' ' << x % 2;", "answer":"3 1", "hint":"Integer division truncates; modulo is the remainder.", "explanation":"7 / 2 is 3 with remainder 1."},
        {"prompt":"int x = 2; cout << x++ << ' ' << x;", "answer":"2 3", "hint":"Post-increment yields the old value before increasing x.", "explanation":"The first output uses 2, then x becomes 3."}]},
    "java-debugger": {"subject":"JAVA", "title":"Java Code Debugger", "mechanic":"code-edit", "objective":"Repair Java logic using boundary-case reasoning.", "instructions":"Replace the marked faulty line. Private, fixed exercise checks validate the answer without compiling or running submitted source.", "levels":[
        {"prompt":"static boolean isPositive(int n) { return n >= 0; }", "task":"Zero is not positive. Fix the condition.", "answer":"return n > 0;", "tests":["isPositive(1) true", "isPositive(0) false"], "hint":"Positive means strictly greater than zero."},
        {"prompt":"int total = 0; for (int value : values) total = value;", "task":"Accumulate every value rather than replacing the total.", "answer":"total += value;", "tests":["[1,2,3] gives 6"], "hint":"Add each current value to the running total."}]},
    "java-oop": {"subject":"JAVA", "title":"Object-Oriented Design Lab", "mechanic":"design-choice", "objective":"Choose a class design that preserves encapsulation and polymorphism.", "instructions":"Read the design constraint and select the best implementation approach.", "levels":[
        {"prompt":"Several payment methods must implement pay(amount), while checkout calls them uniformly.", "choices":["Use a Payment interface implemented by each method", "Put all branches in a public global variable", "Duplicate checkout for every payment type"], "answer":0, "hint":"A shared contract lets checkout depend on behavior rather than concrete classes.", "explanation":"An interface provides a common contract and supports polymorphic dispatch."},
        {"prompt":"A bank account balance must never be set to a negative value directly by callers.", "choices":["Make balance private and validate deposits/withdrawals", "Expose balance as public", "Use a static field shared by every account"], "answer":0, "hint":"Hide state and make changes through validated operations.", "explanation":"Encapsulation protects invariants by controlling access to mutable state."}]},
    "python-debug": {"subject":"PYTHON", "title":"Python Debugging Lab", "mechanic":"code-edit", "objective":"Find and repair common Python logic errors.", "instructions":"Supply the corrected line. Private, fixed exercise checks validate it without evaluating submitted Python.", "levels":[
        {"prompt":"def contains(items, target):\n    for item in items:\n        if item == target:\n            return False\n    return False", "task":"Return True when a matching item is found.", "answer":"return True", "tests":["contains([1,2], 2) is True", "contains([], 2) is False"], "hint":"A match should immediately return the positive result."},
        {"prompt":"def average(values):\n    return sum(values) / len(values)", "task":"Guard against an empty list before dividing.", "answer":"if not values: return 0", "tests":["average([]) returns 0", "average([2,4]) returns 3"], "hint":"Check whether the sequence is empty before using its length as divisor."}]},
    "python-logic": {"subject":"PYTHON", "title":"Python Logic Builder", "mechanic":"logic-builder", "objective":"Build a correct Boolean condition from reusable logic blocks.", "instructions":"Arrange the condition blocks in order to express the required rule.", "levels":[
        {"prompt":"Accept n when it is between 1 and 9 inclusive.", "blocks":["1 <= n", "and", "n <= 9"], "answer":["1 <= n", "and", "n <= 9"], "hint":"Both endpoints are included, so use inclusive comparisons.", "explanation":"A chained inclusive range is equivalent to 1 <= n <= 9."},
        {"prompt":"Accept a user when active is true and the account is not locked.", "blocks":["active", "and", "not locked"], "answer":["active", "and", "not locked"], "hint":"Both requirements must hold at the same time.", "explanation":"AND requires both active and not locked."}]},
    "dsa-arena": {"subject":"DSA", "title":"Algorithm Arena", "mechanic":"order", "objective":"Put algorithm steps in a valid order and observe the invariant.", "instructions":"Arrange the shuffled algorithm steps, then check the sequence.", "levels":[
        {"prompt":"Binary search on a sorted array", "steps":["Set low and high", "Compute midpoint", "Compare midpoint with target", "Discard the half that cannot contain target"], "hint":"Each iteration halves the remaining search interval.", "explanation":"Maintaining bounds and discarding one half gives logarithmic search."},
        {"prompt":"Breadth-first graph traversal", "steps":["Enqueue the start node", "Dequeue the front node", "Visit each unvisited neighbour", "Enqueue those neighbours"], "hint":"BFS uses a FIFO queue.", "explanation":"FIFO processing explores vertices by increasing distance from the start."}]},
    "dsa-visualizer": {"subject":"DSA", "title":"Data Structure Visualizer", "mechanic":"structure-trace", "objective":"Apply operations and predict the resulting stack or queue.", "instructions":"Use the operation controls to build the resulting state; the server validates the final sequence.", "levels":[
        {"prompt":"Start with an empty stack. Apply: push 4, push 9, pop, push 2. Enter bottom-to-top contents.", "operations":["push(4)","push(9)","pop()","push(2)"], "answer":[4,2], "structure":"Stack", "hint":"A stack is last-in, first-out; pop removes the newest item.", "explanation":"After the operations, 4 remains below 2."},
        {"prompt":"Start with an empty queue. Apply: enqueue A, enqueue B, dequeue, enqueue C. Enter front-to-back contents.", "operations":["enqueue(A)","enqueue(B)","dequeue()","enqueue(C)"], "answer":["B","C"], "structure":"Queue", "hint":"A queue is first-in, first-out; dequeue removes the oldest item.", "explanation":"A is removed first, leaving B then C."}]},
    "dbms-sql": {"subject":"DBMS", "title":"SQL Query Lab", "mechanic":"sql-query", "objective":"Construct a query that retrieves the required records.", "instructions":"Enter a query for the displayed schema. Queries are matched against supported patterns and are never run against the app database.", "levels":[
        {"prompt":"Table Students(id, name, gpa). Return names of students with gpa >= 3.5, alphabetically.", "answer":"SELECT name FROM Students WHERE gpa >= 3.5 ORDER BY name;", "hint":"Filter with WHERE, then sort with ORDER BY.", "explanation":"The WHERE clause filters rows before ORDER BY sorts the result."},
        {"prompt":"Table Orders(id, customer_id, total). Return each customer_id and their total spend, highest first.", "answer":"SELECT customer_id, SUM(total) FROM Orders GROUP BY customer_id ORDER BY SUM(total) DESC;", "hint":"Aggregate per customer, then order the aggregate descending.", "explanation":"GROUP BY forms customer groups; SUM aggregates each group."}]},
    "dbms-er": {"subject":"DBMS", "title":"ER Diagram Builder", "mechanic":"er-diagram", "objective":"Connect entities with correct relationship cardinalities.", "instructions":"Select the relationship edges and cardinalities that represent the stated domain.", "levels":[
        {"prompt":"One department employs many employees; each employee belongs to one department.", "choices":["Department 1:N Employee", "Department M:N Employee", "Department 1:1 Employee"], "answer":0, "hint":"One department can relate to multiple employees, each with one department.", "explanation":"The foreign key normally sits on Employee for a one-to-many relationship."},
        {"prompt":"A student can enroll in many courses and each course has many students.", "choices":["Student 1:N Course", "Student M:N Course", "Student 1:1 Course"], "answer":1, "hint":"Both sides can have multiple related records.", "explanation":"A many-to-many relation is represented with an enrollment junction table."}]},
    "os-scheduler": {"subject":"OS", "title":"CPU Scheduling Simulator", "mechanic":"schedule", "objective":"Schedule processes using the selected policy and compare waiting time.", "instructions":"Use the shortest-job-first rule to order processes that arrive at time zero.", "levels":[
        {"prompt":"Non-preemptive SJF. Burst times: P1=6, P2=2, P3=4.", "jobs":["P1 (6)","P2 (2)","P3 (4)"], "answer":["P2","P3","P1"], "hint":"Choose the smallest remaining burst first.", "explanation":"Ascending burst time gives P2, P3, P1."},
        {"prompt":"Non-preemptive SJF. Burst times: A=3, B=8, C=1, D=5.", "jobs":["A (3)","B (8)","C (1)","D (5)"], "answer":["C","A","D","B"], "hint":"Sort all available processes by burst time.", "explanation":"The order is 1, 3, 5, then 8 time units."}]},
    "os-memory": {"subject":"OS", "title":"Memory Allocation Challenge", "mechanic":"memory-allocation", "objective":"Allocate processes with first-fit and account for remaining holes.", "instructions":"Process the requests in order and assign each to the first sufficiently large free block.", "levels":[
        {"prompt":"Blocks [100, 500, 200]. Requests [212, 100]. Enter chosen block indexes (0-based).", "blocks":[100,500,200], "requests":[212,100], "answer":[1,0], "hint":"For each request, scan blocks from the beginning and choose the first large enough.", "explanation":"212 fits first in block 1; the first block still fits 100."},
        {"prompt":"Blocks [300, 120, 450]. Requests [110, 301, 100]. Enter chosen block indexes (0-based).", "blocks":[300,120,450], "requests":[110,301,100], "answer":[0,2,0], "hint":"A block can be reused if its remaining space still fits the next request.", "explanation":"First-fit chooses block 0, then block 2, then reuses the remaining 190 in block 0."}]},
    "cn-routing": {"subject":"CN", "title":"Packet Routing Simulator", "mechanic":"route", "objective":"Route packets over a network while minimizing hop count.", "instructions":"Select the shortest valid route from source to destination.", "levels":[
        {"prompt":"Route A to D. Links: A-B, A-C, B-D, C-E, E-D.", "nodes":["A","B","C","D","E"], "edges":[["A","B"],["A","C"],["B","D"],["C","E"],["E","D"]], "start":"A", "end":"D", "answer":["A","B","D"], "hint":"Compare the number of links in each path.", "explanation":"A-B-D uses two hops; the alternate route uses three."},
        {"prompt":"Route S to T. Links: S-A, A-B, B-T, S-C, C-T.", "nodes":["S","A","B","C","T"], "edges":[["S","A"],["A","B"],["B","T"],["S","C"],["C","T"]], "start":"S", "end":"T", "answer":["S","C","T"], "hint":"The route through C reaches T in two hops.", "explanation":"S-C-T is a shortest path with two links."}]},
    "cn-troubleshoot": {"subject":"CN", "title":"Network Troubleshooting Lab", "mechanic":"diagnose", "objective":"Diagnose a connectivity fault from layered network evidence.", "instructions":"Choose the most likely cause supported by the observations.", "levels":[
        {"prompt":"A host can ping 8.8.8.8 but cannot open example.com. What should you investigate first?", "choices":["DNS resolution", "Ethernet cable", "Default gateway routing", "CPU scheduler"], "answer":0, "hint":"IP connectivity works, but name lookup fails.", "explanation":"Successful IP reachability with hostname failure points to DNS."},
        {"prompt":"A host has an IP address but cannot reach devices outside its subnet; local peers respond.", "choices":["Default gateway configuration", "Browser cache", "DNS only", "Application font"], "answer":0, "hint":"Local communication works, so inspect the route off the subnet.", "explanation":"The default gateway forwards traffic to other networks."}]},
    "web-playground": {"subject":"WEB", "title":"Web Coding Playground", "mechanic":"code-edit", "objective":"Complete a small web coding task and satisfy its prepared checks.", "instructions":"Fill the missing line. Private, fixed exercise checks validate known tasks; the activity does not render or execute arbitrary HTML, CSS or JavaScript.", "levels":[
        {"prompt":"<button id=\"save\">Save</button>\n<!-- Add a line that selects this button -->", "task":"Write the JavaScript selector for the button.", "answer":"const saveButton = document.querySelector('#save');", "tests":["selector targets #save", "selection uses querySelector"], "hint":"Use the button's id with a CSS ID selector."},
        {"prompt":".card {\n  /* Add a declaration to center children horizontally */\n}", "task":"Use flexbox to center the card's children horizontally.", "answer":"display: flex; justify-content: center;", "tests":["display flex", "justify-content center"], "hint":"Enable flex layout, then align items on the main axis."}]},
    "web-ui-debug": {"subject":"WEB", "title":"UI Debugging Challenge", "mechanic":"ui-debug", "objective":"Identify and patch common responsive interface defects.", "instructions":"Choose the smallest CSS or semantic fix that resolves the reported issue.", "levels":[
        {"prompt":"A page overflows on narrow phones because a content panel is fixed at 900px.", "choices":["Use width: min(100%, 900px)", "Set width: 1200px", "Hide the entire page below 600px"], "answer":0, "hint":"Constrain the maximum while allowing the panel to shrink.", "explanation":"A fluid width with a maximum prevents horizontal overflow."},
        {"prompt":"A clickable div cannot be reached with Tab and has no accessible name.", "choices":["Use a button element with a clear label", "Add a larger box-shadow", "Set cursor: pointer only"], "answer":0, "hint":"Use the native interactive element for keyboard and assistive technology support.", "explanation":"A button provides keyboard operation and semantics by default."}]},
    "c-debugger": {"subject":"C", "title":"C Code Debugger", "mechanic":"code-edit", "objective":"Repair a C statement using types and boundary reasoning.", "instructions":"Replace the faulty line. Private, fixed exercise checks validate the answer without compiling or executing submitted code.", "levels":[
        {"prompt":"int max(int a, int b) { return a < b ? a : b; }", "task":"Return the larger of the two values.", "answer":"return a > b ? a : b;", "tests":["max(4, 2) == 4", "max(-1, 0) == 0"], "hint":"The conditional should choose a when a is greater."},
        {"prompt":"char text[4] = \"code\";", "task":"Allocate enough space for four letters and the null terminator.", "answer":"char text[5] = \"code\";", "tests":["four characters plus terminator"], "hint":"C strings need one extra byte for '\\0'."}]},
    "c-memory-trace": {"subject":"C", "title":"C Memory Trace", "mechanic":"output-predict", "objective":"Trace pointer and array behavior without running native code.", "instructions":"Enter the displayed expression's result using C array indexing rules.", "levels":[
        {"prompt":"int a[] = {4, 7, 9}; int *p = a; printf(\"%d\", *(p + 1));", "answer":"7", "hint":"p points to a[0]; adding one advances to a[1].", "explanation":"Pointer arithmetic advances by elements, so *(p+1) is 7."},
        {"prompt":"int a[] = {2, 5, 8}; printf(\"%d\", a[0] + a[2]);", "answer":"10", "hint":"Read the first and third array elements, then add them.", "explanation":"2 + 8 equals 10."}]},
}

GAMES.update({
    "se-requirements": {"subject":"SE", "title":"Requirements Prioritizer", "mechanic":"order", "objective":"Prioritize requirements using user value and delivery dependencies.", "instructions":"Arrange the release steps so foundational dependencies come before dependent features.", "levels":[{"prompt":"A feature depends on authentication and profile storage.","steps":["Define account requirements","Design data model","Implement authentication","Build profile feature"],"hint":"Resolve requirements and foundations before dependent features.","explanation":"The profile feature depends on authentication and its data model."}]},
    "se-test-design": {"subject":"SE", "title":"Test Design Lab", "mechanic":"design-choice", "objective":"Choose a compact test set that covers normal, boundary and invalid cases.", "instructions":"Select the test strategy that best covers the stated behavior.", "levels":[{"prompt":"A function accepts integers from 1 through 100. Which test set gives useful boundary coverage?","choices":["0, 1, 100, 101", "20, 30, 40", "1 only"],"answer":0,"hint":"Include values just outside and exactly at both boundaries.","explanation":"Boundary-value tests check invalid edges and valid endpoints."}]},
    "ai-inference": {"subject":"AI", "title":"Inference Trace", "mechanic":"output-predict", "objective":"Trace a small rule-based inference system.", "instructions":"Apply the facts and rule, then enter the inferred result.", "levels":[{"prompt":"Facts: has_wheels(car), electric(car). Rule: electric(X) AND has_wheels(X) → low_emission(X). What is inferred?","answer":"low_emission(car)","hint":"Substitute car for X; both premises are true.","explanation":"The rule fires because both required facts match car."}]},
    "ai-feature-lab": {"subject":"AI", "title":"Feature Selection Lab", "mechanic":"design-choice", "objective":"Choose features that avoid target leakage and irrelevant inputs.", "instructions":"Select the feature set that is available at prediction time.", "levels":[{"prompt":"Predict whether a loan will default at application time. Which input set is valid?","choices":["Applicant income and credit history at application", "Whether the loan defaulted later", "A post-closure recovery status"],"answer":0,"hint":"Only use information known when the prediction is made.","explanation":"Future outcomes leak the target and cannot be used for a real-time prediction."}]},
    "ml-metric-match": {"subject":"ML", "title":"Metric Match", "mechanic":"design-choice", "objective":"Choose evaluation metrics that fit the task and class balance.", "instructions":"Select the most informative metric for the stated imbalanced classification task.", "levels":[{"prompt":"Only 2% of transactions are fraudulent. Which metric pair gives a better view than accuracy alone?","choices":["Precision and recall", "Training loss only", "Number of features and epochs", "Accuracy only"],"answer":0,"hint":"Measure false alarms and missed positive cases.","explanation":"Precision and recall show the tradeoff between false positives and false negatives."}]},
    "ml-overfit-lab": {"subject":"ML", "title":"Overfit Repair Lab", "mechanic":"diagnose", "objective":"Diagnose generalization gaps and choose a suitable repair.", "instructions":"Select the intervention that most directly addresses the observed problem.", "levels":[{"prompt":"Training score is 99% and validation score is 61%. What is the best first response?","choices":["Use regularization or simplify the model, then validate", "Increase model complexity", "Tune against the validation labels repeatedly until perfect"],"answer":0,"hint":"The model fits training data much better than unseen validation data.","explanation":"Regularization or reduced complexity can improve generalization; repeated validation tuning leaks information."}]},
    "cyber-incident": {"subject":"CYBER", "title":"Incident Response Sequence", "mechanic":"order", "objective":"Put core incident response actions in a defensible order.", "instructions":"Arrange the response steps from initial handling through recovery.", "levels":[{"prompt":"A workstation shows signs of malware infection.","steps":["Identify and record the alert", "Contain the affected host", "Eradicate the malware and root cause", "Restore safely and monitor"],"hint":"Limit spread before removal; verify before returning to service.","explanation":"Identification, containment, eradication and recovery preserve evidence and reduce spread."}]},
    "cyber-phishing": {"subject":"CYBER", "title":"Phishing Defense Lab", "mechanic":"diagnose", "objective":"Identify the safest response to a suspicious message.", "instructions":"Choose the response that protects the account and preserves reporting context.", "levels":[{"prompt":"An email asks you to sign in through an unfamiliar shortened link to avoid account closure.","choices":["Do not open the link; report it through the approved channel", "Reply with your password to verify", "Forward it to everyone for advice"],"answer":0,"hint":"Urgency, credential requests and concealed destinations are warning signs.","explanation":"Avoiding the link and reporting it prevents credential theft and helps responders."}]},
    "cloud-architecture": {"subject":"CLOUD", "title":"Cloud Architecture Builder", "mechanic":"design-choice", "objective":"Choose a resilient design for a stateless web workload.", "instructions":"Select the design that supports health checks and failure recovery.", "levels":[{"prompt":"A stateless web service must remain available when one instance fails.","choices":["Run multiple instances behind a health-checking load balancer", "Use one large instance with no health checks", "Store all session state only in one instance's memory"],"answer":0,"hint":"Avoid a single compute failure point and route around unhealthy instances.","explanation":"Multiple instances and health checks allow traffic to avoid a failed instance."}]},
    "cloud-cost": {"subject":"CLOUD", "title":"Cloud Cost Estimator", "mechanic":"numeric", "objective":"Estimate simple compute cost from rate and runtime.", "instructions":"Multiply the hourly rate by the number of running hours.", "levels":[{"prompt":"A test instance costs $0.20 per hour and runs for 10 hours. Enter total cost in dollars.","answer":2,"hint":"Cost equals hourly rate multiplied by hours.","explanation":"$0.20 × 10 hours = $2.00."}]},
    "embedded-interrupt": {"subject":"EMBEDDED", "title":"Interrupt Trace", "mechanic":"order", "objective":"Order a safe interrupt-service flow.", "instructions":"Arrange the steps so the interrupt handler stays short and defers lengthy work.", "levels":[{"prompt":"A timer interrupt fires while the main loop is running.","steps":["Save required state", "Acknowledge the interrupt source", "Record a minimal event or flag", "Return and process the work in the main loop"],"hint":"Keep the handler bounded and move lengthy work outside it.","explanation":"A brief handler acknowledges and records the event, then defers work."}]},
    "embedded-pinmap": {"subject":"EMBEDDED", "title":"Pin Mapping Challenge", "mechanic":"design-choice", "objective":"Select a safe pin assignment for a simple embedded board.", "instructions":"Choose the mapping that avoids output contention and respects input/output roles.", "levels":[{"prompt":"A sensor provides an analog voltage and an LED needs a digital output.","choices":["Sensor to analog input; LED through a resistor to a digital output", "Sensor to output; LED directly across the supply", "Connect both signals to the same output pin"],"answer":0,"hint":"Measure the sensor with an input and drive the LED with current limiting.","explanation":"An analog input measures the sensor; a resistor limits LED current."}]},
    "iot-protocol": {"subject":"IOT", "title":"IoT Protocol Lab", "mechanic":"design-choice", "objective":"Choose a communication pattern suited to constrained devices.", "instructions":"Select the lightweight publish/subscribe option for intermittent sensor updates.", "levels":[{"prompt":"A battery-powered sensor sends small updates through a broker to multiple subscribers.","choices":["MQTT publish/subscribe", "Raw unframed bytes without addressing", "A desktop-only file transfer"],"answer":0,"hint":"Look for a lightweight broker-based publish/subscribe protocol.","explanation":"MQTT is designed around lightweight publish/subscribe messaging."}]},
    "iot-topology": {"subject":"IOT", "title":"IoT Topology Builder", "mechanic":"route", "objective":"Build a valid path from a sensor to its cloud service.", "instructions":"Select the shortest route using only the available links.", "levels":[{"prompt":"Route Sensor to Cloud. Links: Sensor-Gateway, Gateway-Cloud, Sensor-Phone, Phone-Cloud, Phone-Gateway.","nodes":["Sensor","Gateway","Phone","Cloud"],"edges":[["Sensor","Gateway"],["Gateway","Cloud"],["Sensor","Phone"],["Phone","Cloud"],["Phone","Gateway"]],"start":"Sensor","end":"Cloud","answer":["Sensor","Gateway","Cloud"],"hint":"Choose a valid two-hop route.","explanation":"The Sensor-Gateway-Cloud path uses two links."}]},
})

SUBJECTS = {"C":"C Programming", "CPP":"C++", "JAVA":"Java", "PYTHON":"Python", "DSA":"Data Structures and Algorithms", "DBMS":"Database Management Systems", "OS":"Operating Systems", "CN":"Computer Networks", "WEB":"Web Development", "SE":"Software Engineering", "AI":"Artificial Intelligence", "ML":"Machine Learning", "CYBER":"Cybersecurity", "CLOUD":"Cloud Computing", "EMBEDDED":"Embedded Systems", "IOT":"Internet of Things"}

for _game_id, _levels in EXTRA_LEVELS.items():
    GAMES[_game_id]["levels"].extend(_levels)
for _game_id, _levels in ROTATING_LEVELS.items():
    GAMES[_game_id]["levels"].extend(_levels)

_difficulty_order = {"Easy": 0, "Medium": 1, "Hard": 2, "Expert": 3}
for _game_id, _game in GAMES.items():
    _level_count = len(_game["levels"])
    for _index, _level in enumerate(_game["levels"]):
        if _game_id == "python-logic":
            _level.setdefault("difficulty", ("Easy", "Medium", "Hard", "Expert")[min(_index // 3, 3)])
        elif _level_count >= 4:
            _level.setdefault("difficulty", "Easy" if _index < 2 else "Medium" if _index == 2 else "Hard")
        else:
            _level.setdefault("difficulty", ("Easy", "Medium", "Hard", "Expert")[min(_index, 3)])


def public_game(game_id: str) -> dict | None:
    game = GAMES.get(game_id)
    if not game:
        return None
    levels = []
    for item in game["levels"]:
        clean = {k: v for k, v in item.items() if k not in {"answer", "correct", "target", "target_force", "atoms", "bonds", "x", "y", "required", "positions", "conclusion", "tests", "test_cases"}}
        for key in ("steps", "blocks", "jobs"):
            if key in clean:
                clean[key] = list(clean[key]); random.SystemRandom().shuffle(clean[key])
        if game["mechanic"] == "region-order": clean["regions"] = list(clean["regions"]); random.SystemRandom().shuffle(clean["regions"])
        if game["mechanic"] in {"logic-builder", "order"}:
            key = "blocks" if "blocks" in clean else "steps"
            clean[key] = list(clean[key]); random.SystemRandom().shuffle(clean[key])
        if "events" in clean:
            clean["events"] = list(clean["events"]); random.SystemRandom().shuffle(clean["events"])
        if game["mechanic"] == "circuit": clean["components"] = ["battery", "wire_a", "closed_switch", "wire_b", "resistor", "bulb"]
        if game["mechanic"] == "expression": clean["target"] = item["target"]
        if game["mechanic"] == "evidence":
            clean["conclusions"] = [item["conclusion"], "There is not enough evidence to support a conclusion."]
            random.SystemRandom().shuffle(clean["conclusions"])
        levels.append(clean)
    return {"id": game_id, "subject": game["subject"], "subject_name": SUBJECTS[game["subject"]],
            "title": game["title"], "mechanic": game["mechanic"], "objective": game["objective"],
            "instructions": game["instructions"], "level_count": len(levels), "levels": levels}


def initial_state(game_id: str, previous_order: list[int] | None = None, *, previous_last: int | None = None) -> dict:
    if game_id not in GAMES:
        raise ValueError("Unknown game.")
    levels = GAMES[game_id]["levels"]
    if previous_last is not None:
        previous_order = [previous_last]
    rng = random.SystemRandom()
    session_size = min(4, len(levels))
    previous = {index for index in (previous_order or []) if isinstance(index, int) and 0 <= index < len(levels)}
    available = [index for index in range(len(levels)) if index not in previous]
    rng.shuffle(available)
    # Include as many unseen levels as possible, then fill the rest from the
    # bank. With a six-level bank this makes two levels new on each replay.
    unseen_count = min(session_size // 2, len(available))
    selected = available[:unseen_count]
    remaining = [index for index in range(len(levels)) if index not in selected]
    rng.shuffle(remaining)
    selected.extend(remaining[:session_size - len(selected)])
    buckets = {}
    for index in selected:
        difficulty = levels[index].get("difficulty", "Easy")
        buckets.setdefault(difficulty, []).append(index)
    order = []
    for difficulty in sorted(buckets, key=lambda value: _difficulty_order.get(value, 99)):
        rng.shuffle(buckets[difficulty])
        order.extend(buckets[difficulty])
    return {"level": 0, "level_order": order, "score": 0, "mistakes": 0, "actions": 0, "complete": False, "events": []}


def public_session_game(game_id: str, state: dict) -> dict:
    """Return sanitized game content in the same order as this session."""
    game = public_game(game_id)
    order = state.get("level_order") if isinstance(state, dict) else None
    if not isinstance(order, list) or not order or len(set(order)) != len(order) or any(not isinstance(index, int) or index < 0 or index >= len(game["levels"]) for index in order):
        return game
    game["levels"] = [game["levels"][index] for index in order]
    game["level_count"] = len(game["levels"])
    return game


def _safe_expression(expression: str, values: list[int], operators: list[str], target: int) -> bool:
    if len(expression) > 80 or not re.fullmatch(r"[0-9+*()\s-]+", expression):
        return False
    try:
        root = ast.parse(expression, mode="eval").body
    except SyntaxError:
        return False
    nums = [int(x) for x in re.findall(r"\d+", expression)]
    ops = re.findall(r"[+*()-]", expression)
    if sorted(nums) != sorted(values) or any(op not in operators and op not in "()" for op in ops):
        return False
    def calc(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, int): return n.value
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add): return calc(n.left) + calc(n.right)
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mult): return calc(n.left) * calc(n.right)
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Sub): return calc(n.left) - calc(n.right)
        raise ValueError
    try: return calc(root) == target
    except (ValueError, TypeError): return False


def apply_action(game_id: str, state: dict, action: dict) -> tuple[dict, dict]:
    """Apply one action and return (new state, public feedback)."""
    if game_id not in GAMES or not isinstance(action, dict):
        raise ValueError("Invalid game action.")
    if state.get("complete"):
        raise ValueError("This session is already complete.")
    game = GAMES[game_id]
    level = int(state.get("level", 0))
    order = state.get("level_order")
    if not isinstance(order, list) or not order or len(set(order)) != len(order) or any(not isinstance(index, int) or index < 0 or index >= len(game["levels"]) for index in order):
        order = list(range(len(game["levels"])))
    if level >= len(order):
        state["complete"] = True
        return state, {"complete": True, "correct": True, "message": "All levels complete."}
    task_index = order[level]
    task = game["levels"][task_index]
    mechanic = game["mechanic"]
    correct = False
    value = action.get("value")
    try:
        if mechanic == "numeric": correct = math.isclose(float(value), float(task["answer"]), abs_tol=1e-8)
        elif mechanic == "expression": correct = _safe_expression(str(value), task["tiles"], task["operators"], task["target"])
        elif mechanic == "simulation":
            mass, acceleration = float(action.get("mass")), float(action.get("acceleration"))
            force = mass * acceleration
            guess = float(value)
            correct = 0 < mass <= 20 and 0 < acceleration <= 20 and math.isclose(guess, force)
            value = {"mass": mass, "acceleration": acceleration, "force": force}
        elif mechanic == "circuit":
            components = set(value.get("components", [])) if isinstance(value, dict) else set()
            edges = value.get("connections", []) if isinstance(value, dict) else []
            known = {"battery", "closed_switch", "resistor", "bulb", "wire_a", "wire_b"}
            valid_edges = {tuple(sorted((a, b))) for a in known for b in known if a != b}
            chosen = [tuple(sorted(edge)) for edge in edges if isinstance(edge, list) and len(edge) == 2]
            degrees = {node: 0 for node in components}
            for a, b in chosen:
                if a not in components or b not in components or (a, b) not in valid_edges: break
                degrees[a] += 1; degrees[b] += 1
            connected = set()
            if components:
                stack = [next(iter(components))]
                while stack:
                    node = stack.pop()
                    if node in connected: continue
                    connected.add(node)
                    stack.extend(other for a, b in chosen for other in ([b] if a == node else [a] if b == node else []))
            correct = (set(task["required"]) <= components <= known and len(chosen) == len(edges)
                       and len(chosen) == len(components) and len(set(chosen)) == len(chosen)
                       and bool(components) and all(degree == 2 for degree in degrees.values())
                       and connected == components)
        elif mechanic == "atoms": correct = isinstance(value, dict) and value.get("atoms") == task["atoms"] and value.get("bonds") == task["bonds"]
        elif mechanic == "reaction": correct = isinstance(value, list) and value == task["answer"]
        elif mechanic == "label": correct = isinstance(value, dict) and all(value.get(label) == task["positions"][label] for label in task["labels"])
        elif mechanic == "ecosystem":
            food = int(action.get("food", 0)); habitat = int(action.get("habitat", 0))
            if not 0 <= food <= 10 or not 0 <= habitat <= 10: raise ValueError("Resource settings must be from 0 to 10.")
            herbivores = max(0, min(20, food + 2))
            predators = max(0, min(10, habitat // 2 + 1 + (1 if herbivores >= 8 else 0)))
            populations = [herbivores, predators]
            correct = populations == task["target"]; value = {"food": food, "habitat": habitat, "populations": populations}
        elif mechanic == "code-edit": correct = code_checks.validate_code_edit(game_id, task_index, value, task["answer"])
        elif mechanic == "output-predict": correct = isinstance(value, str) and value.strip() == task["answer"]
        elif mechanic == "design-choice" or mechanic in {"er-diagram", "diagnose", "ui-debug"}:
            correct = isinstance(value, int) and not isinstance(value, bool) and value == task["answer"]
        elif mechanic == "logic-builder": correct = isinstance(value, list) and value == task["answer"]
        elif mechanic == "structure-trace": correct = isinstance(value, list) and value == task["answer"]
        elif mechanic == "sql-query":
            normalize = lambda q: re.sub(r"\s+", " ", str(q).strip().rstrip(";")).lower()
            correct = normalize(value) == normalize(task["answer"])
        elif mechanic == "schedule":
            expected = sorted((job.split()[0] for job in task["jobs"]), key=lambda name: int(next(x.split("(")[1].rstrip(")") for x in task["jobs"] if x.startswith(name))))
            correct = isinstance(value, list) and value == expected
        elif mechanic == "memory-allocation":
            remaining = list(task["blocks"]); expected = []
            for request_size in task["requests"]:
                found = next((i for i, size in enumerate(remaining) if size >= request_size), None)
                expected.append(found)
                if found is not None: remaining[found] -= request_size
            correct = isinstance(value, list) and value == expected and expected == task["answer"]
        elif mechanic == "route":
            path = value if isinstance(value, list) else []
            edges = {frozenset(edge) for edge in task["edges"]}
            valid_path = len(path) >= 2 and path[0] == task["start"] and path[-1] == task["end"] and all(frozenset(path[i:i+2]) in edges for i in range(len(path)-1))
            correct = valid_path and path == task["answer"]
        elif mechanic in ("order", "story-order", "timeline", "region-order"):
            expected = task.get("steps", task.get("blocks", task.get("events", task.get("regions"))))
            if mechanic == "timeline": expected = [f'{x["name"]} ({x["year"]})' for x in sorted(task["events"], key=lambda x: x["year"])]
            correct = isinstance(value, list) and value == expected
        elif mechanic == "letters": correct = isinstance(value, str) and value.strip().upper() == task["answer"] and sorted(value.strip().upper()) == sorted(task["letters"])
        elif mechanic == "evidence": correct = isinstance(value, dict) and sorted(value.get("evidence", [])) == task["correct"] and value.get("conclusion") == task["conclusion"]
        elif mechanic == "map-click": correct = isinstance(value, dict) and value.get("x") == task["x"] and value.get("y") == task["y"]
    except (TypeError, ValueError, OverflowError):
        correct = False
    state["actions"] = int(state.get("actions", 0)) + 1
    if correct:
        state["score"] = int(state.get("score", 0)) + 100
        state["level"] = level + 1
        state["complete"] = state["level"] >= len(order)
        message = "Correct. " + (f"All {code_checks.suite_size(game_id, task_index)} private test cases passed. " if mechanic == "code-edit" else "") + task.get("explanation", "Your solution satisfies the task requirements.") + (" Level complete." if not state["complete"] else " You completed the game!")
    else:
        state["mistakes"] = int(state.get("mistakes", 0)) + 1
        message = "Not yet. " + task.get("hint", "Review the objective and try again.")
    if mechanic == "simulation" and isinstance(value, dict): message += f" Calculated force: {value['force']:g} N."
    if mechanic == "ecosystem" and isinstance(value, dict): message += f" Simplified model populations: {value['populations'][0]} {task['species'][0]}, {value['populations'][1]} {task['species'][1]}."
    if mechanic == "circuit" and correct: message += " The connected loop is closed and the bulb lights."
    if mechanic == "atoms" and correct: message += f" The supported molecule {task['formula']} has a valid atom count and bond pattern."
    if mechanic == "reaction" and correct: message += " Atom counts are balanced on both sides."
    state["events"].append({"level": level, "correct": correct, "value": value})
    return state, {"correct": correct, "complete": state["complete"], "score": state["score"], "mistakes": state["mistakes"], "level": state["level"], "message": message}
