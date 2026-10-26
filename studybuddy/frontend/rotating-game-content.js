/* Supplemental authored content used by the browser-local game catalog. */
const STUDY_ROTATING_GAME_CONTENT = {
  RAW: {
    C: [
      ['Pointers','What does a pointer arithmetic expression p + 1 advance by?',['One byte','One element of the pointed-to type','The whole array','One bit'],1,'Pointer arithmetic advances by the size of the pointed-to type.'],
      ['Arrays','For an array of length n, what is its final valid index?',['n','n - 1','n + 1','1'],1,'Zero-based indexing makes n - 1 the final valid position.']],
    CPP: [
      ['Ownership','What is the main benefit of RAII?',['Resources follow object lifetime','Every allocation becomes global','Exceptions are disabled','Pointers become integers'],0,'RAII ties resource release to object lifetime.'],
      ['Containers','When is std::vector a good fit?',['Dynamic contiguous sequence','Unique sorted keys only','FIFO task queue only','Fixed-size linked nodes'],0,'A vector offers dynamic size and contiguous storage.']],
    JAVA: [
      ['Equality','How should two String values be compared by content?',['==','equals','hashCode only','compare reference addresses'],1,'String.equals compares character contents.'],
      ['Collections','Which map operation supplies a fallback for a missing key?',['getOrDefault','push','append','poll'],0,'Map.getOrDefault returns a provided fallback when a key is absent.']],
    DSA: [
      ['Heaps','What is the time complexity of removing the root from a binary heap?',['O(1)','O(log n)','O(n)','O(n log n)'],1,'After removal, heap order is restored by a logarithmic sift.'],
      ['Graphs','Which traversal finds shortest paths in an unweighted graph?',['Depth-first search','Breadth-first search','Heap sort','Binary search'],1,'BFS explores vertices in increasing edge distance.']],
    DBMS: [
      ['Transactions','What does isolation protect against?',['Interference between concurrent transactions','Disk failure only','Invalid column names','Slow network links'],0,'Isolation controls how concurrent work can observe each other.'],
      ['Indexes','What is a common cost of adding an index?',['Writes must maintain extra index data','Rows lose their primary keys','Queries cannot filter values','Transactions stop being atomic'],0,'Indexes speed some reads but add storage and write-maintenance cost.']],
    OS: [
      ['Deadlocks','Which condition means a resource cannot be forcibly taken from its holder?',['Mutual exclusion','Hold and wait','No preemption','Circular wait'],2,'No preemption means resources are released voluntarily.'],
      ['Virtual memory','What does a page fault indicate?',['A needed page is not currently mapped in RAM','The CPU has no registers','A process has ended','A disk is formatted'],0,'The operating system must resolve the missing page mapping.']],
    CN: [
      ['TCP','What does a TCP acknowledgement confirm?',['Receipt of sequence-numbered data','A DNS record is cached','A route is permanent','A port is encrypted'],0,'Acknowledgements let TCP track received bytes and retransmit missing data.'],
      ['DNS','What does a DNS resolver return for a successful address lookup?',['A name-to-record result such as an IP address','A transport-layer port','A Wi-Fi password','A file-system path'],0,'DNS resolves names to records, commonly IP addresses.']],
    PYTHON: [
      ['Defaults','Why avoid a mutable list as a function default?',['The same object is reused between calls','Lists cannot be returned','The function becomes asynchronous','The list is always empty'],0,'Default expressions are evaluated once, so a mutable object can retain state.'],
      ['Generators','What does yield do in a generator?',['Produces a value and suspends the function','Deletes the current frame','Sorts all future values','Declares a class'],0,'yield returns a value while preserving generator state for the next request.']],
    WEB: [
      ['DOM','Why use textContent for untrusted text?',['It inserts text without parsing it as HTML','It automatically sends a request','It styles the element','It validates a password'],0,'textContent avoids interpreting supplied text as markup.'],
      ['Accessibility','What should a custom keyboard control provide?',['Keyboard operation and an accessible name','A pointer cursor only','A decorative shadow','An animation on hover'],0,'Keyboard access and a clear name make controls usable beyond a mouse.']],
    SE: [
      ['Requirements','What makes an acceptance criterion useful?',['It describes an observable result','It uses vague words only','It is hidden from testers','It changes after every build'],0,'Observable criteria let the team verify whether the requirement is met.'],
      ['Testing','What does a regression test check?',['Previously working behavior still works after a change','Only the source-code color','The product name is unchanged','Every test is slow'],0,'Regression checks catch unintended breaks in existing behavior.']],
    AI: [
      ['Evaluation','What is data leakage in a prediction task?',['Using information unavailable at prediction time','Removing duplicate rows','Splitting data before training','Logging model versions'],0,'Leaked future or target information makes evaluation misleading.'],
      ['Search','What does an admissible A* heuristic guarantee?',['It never overestimates remaining cost','It always returns the first neighbor','It ignores path cost','It sorts the input'],0,'A lower-bound heuristic preserves optimality under standard A* conditions.']],
    ML: [
      ['Evaluation','For rare positive cases, why can accuracy be misleading?',['A model can predict the majority class and still score highly','Accuracy measures memory use','Accuracy is always zero','Accuracy ignores all negatives'],0,'Class imbalance can hide poor detection of the rare class.'],
      ['Validation','What is a validation set used for?',['Choosing model settings without using the final test set','Replacing all training data','Encoding every feature as text','Guaranteeing perfect results'],0,'Validation supports model selection while the test set stays reserved.']],
    CYBER: [
      ['Access control','What does least privilege mean?',['Give only the access needed for a task','Share one administrator password','Keep every account permanently active','Disable audit logs'],0,'Limiting permissions reduces the damage from mistakes or compromise.'],
      ['Phishing','What is the safest response to an unexpected credential link?',['Verify through a known channel and report it','Open it quickly before it expires','Reply with a password','Forward it to everyone'],0,'Independent verification avoids the suspicious link and supports reporting.']],
    CLOUD: [
      ['Reliability','Why spread service instances across failure zones?',['A single-zone outage is less likely to stop the service','It removes the need for backups','It guarantees zero latency','It disables health checks'],0,'Independent zones reduce the impact of one location failing.'],
      ['Storage','What is object storage commonly used for?',['Durable files and unstructured blobs','CPU scheduling','SQL transaction locks','In-memory stack frames'],0,'Object storage is suited to durable file-like objects at scale.']],
    EMBEDDED: [
      ['Interrupts','Why should an interrupt handler stay short?',['To keep response latency bounded','To allocate unlimited memory','To block the main loop forever','To print every sensor sample'],0,'Short handlers reduce latency and defer heavier work safely.'],
      ['Inputs','What does switch debouncing address?',['Rapid contact changes around a press','A low battery voltage','A compiler warning','A network route'],0,'Mechanical contacts can flicker briefly before settling.']],
    IOT: [
      ['Messaging','Why include a sequence number in telemetry?',['Consumers can detect ordering and duplicates','The payload becomes encrypted automatically','The device needs no identity','The network stops dropping packets'],0,'A stable sequence helps consumers identify repeated or out-of-order messages.'],
      ['Reliability','What is bounded retry backoff?',['Retries wait longer up to a configured limit','Messages are resent with no delay forever','Every error is ignored','The device changes its identity'],0,'Bounded backoff limits retry load while allowing recovery.']]
  },
  FCR: {
    C: [['Pointer arithmetic','It advances in units of the pointed-to type.','What does p + 1 mean for an int pointer?'],['Array bound','The final valid index is length minus one.','What is the last valid index in a zero-based array of length n?']],
    CPP: [['RAII','Resource cleanup follows object lifetime.','What does RAII connect?'],['Vector','A resizable contiguous sequence.','What does std::vector provide?']],
    JAVA: [['String equality','Use equals to compare String contents.','How do you compare Java String values by content?'],['Map fallback','getOrDefault returns a value when a key is absent.','Which Map method supports a fallback value?']],
    DSA: [['Heap removal','O(log n), because the heap is restored after removing the root.','What is the usual time cost to remove a binary heap root?'],['Unweighted shortest path','Breadth-first search explores one edge-distance layer at a time.','Which traversal finds shortest paths in an unweighted graph?']],
    DBMS: [['Isolation','It controls visibility among concurrent transactions.','What does transaction isolation address?'],['Index trade-off','Indexes use storage and add work to writes.','What cost can an index add?']],
    OS: [['No preemption','A resource cannot be forcibly taken from its holder.','What is the no-preemption deadlock condition?'],['Page fault','The requested page needs operating-system handling.','What does a page fault signal?']],
    CN: [['TCP acknowledgement','It confirms receipt of sequence-numbered data.','What does a TCP acknowledgement help track?'],['DNS','It resolves a name to records such as an IP address.','What does DNS resolution return?']],
    PYTHON: [['Mutable defaults','A mutable default object can be shared across calls.','Why avoid a list as a Python function default?'],['Generator yield','It produces a value and suspends generator state.','What does yield do?']],
    WEB: [['textContent','It inserts text without parsing it as HTML.','Why use textContent for untrusted text?'],['Keyboard controls','They need keyboard operation and an accessible name.','What should a custom keyboard control provide?']],
    SE: [['Acceptance criterion','It states an observable, verifiable result.','What makes an acceptance criterion testable?'],['Regression test','It checks that existing behavior still works after a change.','What does a regression test protect?']],
    AI: [['Data leakage','It uses information unavailable when a prediction is made.','What makes evaluation data leakage?'],['Admissible heuristic','It does not overestimate the remaining cost.','What property supports optimal A* search?']],
    ML: [['Imbalanced accuracy','A majority-only model can score well while missing positives.','Why can accuracy mislead on rare positive cases?'],['Validation set','It supports model selection while the test set remains reserved.','What is a validation set for?']],
    CYBER: [['Least privilege','Give only the permissions a task needs.','What is least privilege?'],['Suspicious link','Verify independently and report through the approved channel.','How should an unexpected credential link be handled?']],
    CLOUD: [['Failure zones','Independent zones reduce the impact of a single-zone outage.','Why spread instances across zones?'],['Object storage','Durable file-like objects and unstructured blobs.','What is object storage suited to?']],
    EMBEDDED: [['Short interrupt handlers','They keep response time bounded and defer lengthy work.','Why keep an interrupt handler short?'],['Debouncing','It filters rapid contact changes around a mechanical press.','What does switch debouncing solve?']],
    IOT: [['Sequence number','It helps identify duplicates and message ordering.','Why add a sequence number to telemetry?'],['Bounded backoff','It increases retry delay only up to a configured maximum.','What does bounded retry backoff mean?']]
  },
  BUILDER: {
    C: [['Build a checked array sum','Order the lines to sum values only after validating the pointer.',['if (values == NULL) return 0;','int sum = 0;','for (size_t i = 0; i < length; ++i) {','sum += values[i];','}','return sum;']],['Build a bounded string scan','Order the lines so the scan stops at the terminator.',['size_t i = 0;',"while (text[i] != '\\0') {",'++i;','}','return i;']]],
    CPP: [['Build a safe vector lookup','Order the lines to return a value only when the index exists.',['if (index >= values.size()) return false;','result = values[index];','return true;']],['Build an RAII output path','Order the lines to open, validate, and write a file.',['std::ofstream output(path);','if (!output) return false;',"output << value << '\\n';",'return output.good();']]],
    JAVA: [['Build a safe list lookup','Order the lines to check the index before reading.',['if (index < 0 || index >= values.size()) return null;','return values.get(index);']],['Build a try-with-resources read','Order the lines to close the reader automatically.',['try (BufferedReader reader = Files.newBufferedReader(path)) {','return reader.readLine();','}']]],
    PYTHON: [['Build a safe dictionary counter','Order the lines to count each word.',['counts = {}','for word in words:','counts[word] = counts.get(word, 0) + 1','return counts']],['Build a bounded binary search','Order the lines to move the search interval.',['mid = (low + high) // 2','if values[mid] < target:','low = mid + 1','else:','high = mid - 1']]],
    DSA: [['Build a cycle-safe DFS step','Order the lines to visit each neighbor once.',['if neighbour not in visited:','visited.add(neighbour)','stack.append(neighbour)']],['Build a stable merge step','Order the lines to take the smaller front item.',['if left[i] <= right[j]:','merged.append(left[i])','i += 1','else:','merged.append(right[j])','j += 1']]],
    WEB: [['Build a safe form submit handler','Order the lines to stop reload and read form data.',['form.addEventListener("submit", event => {','event.preventDefault();','const data = new FormData(form);','save(data);','});']],['Build a keyboard accessible toggle','Order the lines to update a button state.',['button.addEventListener("click", () => {','const expanded = button.getAttribute("aria-expanded") === "true";','button.setAttribute("aria-expanded", String(!expanded));','panel.hidden = expanded;','});']]]
  },
  FILL: {
    C: [['Safe array access','Complete the boundary check before values[index].',['if (index < length)','if (index <= length)','if (index > length)','if (length == 0)'],0,'A valid zero-based index is strictly less than the length.'],['Null allocation check','Complete the allocation failure check.',['if (buffer == NULL)','if (buffer > 0)','if (sizeof(buffer))','if (buffer != 0) free(buffer)'],0,'malloc reports failure by returning NULL.']],
    CPP: [['Vector bounds','Complete the safe index guard.',['if (index >= values.size()) return false;','if (index > values.size()) return false;','if (index == values.size() - 1) return false;','if (values.empty()) index = 0;'],0,'The index must be smaller than the vector size.'],['Map lookup','Complete the iterator validity check.',['if (it != values.end())','if (it != nullptr)','if (values.size() > it)','if (it->second != end)'],0,'A failed map lookup returns the end iterator.']],
    JAVA: [['List bounds','Complete the valid index guard.',['if (index >= 0 && index < values.size())','if (index <= values.size())','if (index > 0 || index < values.size())','if (values.size() > 0)'],0,'A valid list index is non-negative and less than size.'],['String contents','Complete a null-safe text comparison.',['Objects.equals(first, second)','first == second','first.compare(second)','first = second'],0,'Objects.equals handles null and compares values.']],
    PYTHON: [['Dictionary fallback','Complete a missing-key-safe count lookup.',['counts.get(key, 0)','counts[key, 0]','counts.default(key)','counts.value(key, 0)'],0,'dict.get accepts a fallback for absent keys.'],['Empty average','Complete the guard before dividing by len(values).',['if not values: return 0','if values: return 0','if len(values) < 0: return 0','return sum(values)'],0,'Handle the empty sequence before division.']],
    DSA: [['BFS discovery','Complete the step that schedules a newly discovered neighbor.',['queue.append(neighbour)','stack.pop()','queue.sort()','visited.remove(neighbour)'],0,'BFS uses a FIFO queue to explore the next layer.'],['Binary search update','Complete the update when values[mid] is too small.',['low = mid + 1','high = mid + 1','low = mid - 1','return mid'],0,'The midpoint and every smaller value can be discarded.']],
    WEB: [['Safe text update','Complete a text-only update with user supplied content.',['message.textContent = value;','message.innerHTML = value;','message.execute(value);','message.html(value);'],0,'textContent inserts a string without parsing markup.'],['Fetch response','Complete JSON parsing from a Response.',['const data = await response.json();','const data = await response.JSON();','const data = JSON.fetch(response);','const data = response.parse();'],0,'Response.json() parses the response body.']]
  }
};

if (typeof window !== 'undefined') window.STUDY_ROTATING_GAME_CONTENT = STUDY_ROTATING_GAME_CONTENT;
if (typeof module !== 'undefined' && module.exports) module.exports = STUDY_ROTATING_GAME_CONTENT;
