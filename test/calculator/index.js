// Example function:
function greet(name) {
  return `Hello, ${name}!`;
}

// Example class:
class Calculator {
  constructor() {
    this.result = 0;
  }

  add(a, b) {
    this.result = a + b;
    return this.result;
  }

  subtract(a, b) {
    this.result = a - b;
    return this.result;
  }
}

// Exporting functions, classes, or objects to be used by other modules
module.exports = {
  greet,
  Calculator
};
