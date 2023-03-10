# Scripting Language ![Python](https://skillicons.dev/icons?i=python)
Custom scripting language using Python (in development)

### How to run the interpreter
```
cd src && python main.py <file>
```

### Features
- [x] set x = 1
- [x] let y
- [x] const z = 1
- [x] x = 1
- [x] print
- [x] math operations and str concatenation
- [x] for loop
- [x] comments (# single-line and ### multi-line)
- [x] functions
- [x] ternary operator
- [x] str, int, bool and none types
- [x] log function for debugging
- [x] shell mode
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
fn my_function[str, n]
    print str, n

const start = 0
const end = start + 10
let x

set step_str = 'two'
x = step_str == 'one' ? 1 : 2

log x

for i from start to end step x
    my_function 'number:', i
```

### Output
```
x = 2 (int)
number: 0
number: 2
number: 4
number: 6
number: 8
number: 10
```

### Run Tests
```
cd tests && python -m unittest discover
```
