<!DOCTYPE html>

<html>
<head>
  <title>Insight data challenge-Kun</title>
</head>

<body>
  <h1>Insight data challenge</h1>

  <p>The problem has two parts:</p>

  <ol>
    <li>Keep record of previous donation to identify repeat donor</li>

    <li>Keep record of donation stats for each candidate in each zip in each year. So we
    can calculate new stat and print after we identify donor in part 1</li>
  </ol>

  <h2>Identify repeat donor</h2>

  <p>For this task, a unique pair of name and zipcode identifies a donor, we need to see
  if this guy appeared and if his earliest donation is earlier than this record.</p>

  <p>This calls for use of associative dictionary, we can use "name+zipcode" as key and
  earliest donation year as value.<br></p>

  <p>std::unordered_map&lt;string, size_t&gt; would do nicely</p>

  <h2>Keep stat for combinations of candidate, zip and year</h2>

  <p>There is three stat I need to output: sum, count and percentile. First two is easy,
  percentile means that I need to store all eligible records.<br></p>

  <h3>Percentile computation<br></h3>

  <p>Percentile calculation needs a sorted array. But such array is expensive to insert
  into. However, inserting a new element will at most change the percentile position by
  one.<br></p>

  <p>So we can store the data in two priority queues, one with values smaller than
  percentile, other with smallest value at percentile. I just need to maintain correct
  size of the lower part after insertion.<br></p>

  <h3>Data structure</h3>

  <p>class candidateZipYear {</p>

  <p>private:</p>

  <p>&nbsp; static int percentile;<br></p>

  <p>&nbsp; size_t count;</p>

  <p>&nbsp; double sum;</p>

  <p>&nbsp; std::priority_queue&lt;int&gt; lower_part;</p>

  <p>&nbsp; std::priority_queue&lt;int, std::greater&lt;int&gt;&gt; upper_part;</p>

  <p>public:</p>

  <p>&nbsp; candidateZipYear()</p>

  <p>&nbsp; void insert(double);</p>

  <p>&nbsp; std::vector&lt;int&gt; output();</p>

  <p>};</p>

  <h2>Input Validation</h2>

  <h3>Percentile</h3>

  <p>Should be an integer between 0-100</p>

  <h3>Name</h3>

  <p>This is a hard one because name can't be malformed. US has few law governing names
  and you can use non-English characters, numbers, symbols and so on. See
  https://en.wikipedia.org/wiki/Naming_in_the_United_States</p>

  <p>But for the challenge, I made up some requirements to root out "unusual" names a-z
  A-Z .&amp;,'() - is allowed and others busted.</p>

  <h3>ZIP and date</h3>

  <p>zip should be 5-9 digit number. Date should be 8 digits</p>

  <h2>Additional comment</h2>

  <p>The program is written in python in the end because<br></p>

  <ul>
    <li>I need to brush up my python skills</li>

    <li>It's probably I/O bottlenecked anyway</li>

    <li>Writing a csv parser seems lots of coding. You probably want to
    std::getline(your_file, this_line) then std::stringstream row(this_line) then put
    std::getline(row, unit, '|') in a while loop to push unit back to a vector<br></li>
  </ul>
</body>
</html>

