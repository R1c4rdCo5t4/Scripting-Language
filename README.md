# Scripting Language ![Python](https://skillicons.dev/icons?i=python)
Attempt of a custom scripting language using Python

### How to run the interpreter
```
python main.py <file>
```

### Features
- [x] set x = 1
- [x] let y
- [x] const z = 1
- [x] x = 1
- [x] print
- [x] math operations and str concatenation
- [x] for loop
- [x] comments (# and ###)
- [x] functions
- [ ] string formatting
- [ ] while
- [ ] loop 10
- [ ] if-else
- [ ] lists
- [ ] list and str slicing
- [ ] built-in functions (len, sum, enum, max, ...)
- [ ] maps
- [ ] lambda functions
- [ ] list comprehensions
- [ ] classes
- [ ] ...


### Example Code
```
fn my_function(n)
    print('number:', n)

const start = 0
const end = 10
let step

set step_str = 'two'
step = step_str == 'one' ? 1 : 2
log(step)

for i from start to end by step
    my_function(i)
```

### Output
```
step = 2 (int)
number: 0
number: 2
number: 4
number: 6
number: 8
number: 10
```

