---
marp: true
theme: default
paginate: true
<!-- _class: lead -->
<!-- _paginate: skip -->
# Week 5: High-Level Programming with JavaScript

---

## The Journey from Low-Level to High-Level

**The Problem with Low-Level Languages:**
- C requires 500+ lines for a simple web server
- Manual memory management prone to errors
- Complex string handling and buffer management
- Takes weeks to build basic functionality

**High-Level Languages Solve This:**
- JavaScript: 20 lines for the same web server
- Automatic memory management (garbage collection)
- Built-in data structures and APIs
- Hours instead of weeks for development

**Key Insight:** High-level languages manage complexity so developers can focus on business logic, not implementation details.

---

## What is JavaScript?

**JavaScript** is a high-level, interpreted programming language that runs in browsers and on servers (Node.js). Created in 1995 by Brendan Eich at Netscape, it has become the lingua franca of the web.

**Key Characteristics:**
- **Interpreted:** No compilation step required
- **Dynamic typing:** Variables can hold any type
- **First-class functions:** Functions are values that can be passed around
- **Prototype-based:** Object inheritance through prototypes
- **Event-driven:** Designed for asynchronous operations
- **Multi-paradigm:** Supports procedural, object-oriented, and functional programming

---

## JavaScript's Role in Web Development

**The Web Technology Stack:**
- **HTML:** Structure and content
- **CSS:** Styling and layout
- **JavaScript:** Behavior and interactivity

**JavaScript's Unique Position:**
- Only language that runs natively in all browsers
- Both client-side (browser) and server-side (Node.js)
- Powers interactive web applications
- Enables Single Page Applications (SPAs)

**Market Reality (2025):**
- 98% of websites use JavaScript
- #1 most used programming language (GitHub)
- Node.js powers millions of servers worldwide

---

## JavaScript Basics: Variables and Types

**Dynamic Typing:**
```javascript
let message = "Hello";        // String
let count = 42;               // Number
let isActive = true;          // Boolean
let items = [1, 2, 3];        // Array
let user = {name: "Sarah"};   // Object
let nothing = null;           // Null
let notDefined;               // Undefined
```

**Variable Declarations:**
- `var` - Function-scoped (old style, avoid)
- `let` - Block-scoped, can be reassigned
- `const` - Block-scoped, cannot be reassigned

**Type Coercion:**
```javascript
"5" + 3      // "53" (string concatenation)
"5" - 3      // 2 (numeric subtraction)
Boolean("")  // false
Boolean("hello") // true
```

---

## Functions in JavaScript

**Function Declarations:**
```javascript
function greet(name) {
    return "Hello, " + name;
}

// Arrow function (ES6+)
const greet = (name) => "Hello, " + name;

// Function as value
const sayHello = greet;
sayHello("World");  // "Hello, World"
```

**Higher-Order Functions:**
```javascript
const numbers = [1, 2, 3, 4, 5];

// Map: transform each element
const doubled = numbers.map(n => n * 2);  // [2, 4, 6, 8, 10]

// Filter: keep elements that match
const evens = numbers.filter(n => n % 2 === 0);  // [2, 4]

// Reduce: accumulate into single value
const sum = numbers.reduce((acc, n) => acc + n, 0);  // 15
```

---

## Objects and Arrays

**Objects (Key-Value Pairs):**
```javascript
const person = {
    name: "Sarah",
    age: 25,
    skills: ["JavaScript", "Python"],

    // Method
    introduce() {
        return `Hi, I'm ${this.name}`;
    }
};

// Access properties
console.log(person.name);        // "Sarah"
console.log(person["age"]);      // 25
console.log(person.introduce()); // "Hi, I'm Sarah"
```

**Destructuring:**
```javascript
const {name, age} = person;  // Extract properties
const [first, second] = [1, 2, 3];  // Extract array elements
```

---

## Array Methods and Iteration

**Essential Array Methods:**
```javascript
const fruits = ["apple", "banana", "orange"];

// Add/remove elements
fruits.push("grape");      // Add to end
fruits.pop();              // Remove from end
fruits.unshift("mango");   // Add to start
fruits.shift();            // Remove from start

// Iteration
fruits.forEach(fruit => console.log(fruit));

// Find elements
const found = fruits.find(f => f.startsWith("b"));  // "banana"
const hasApple = fruits.includes("apple");          // true

// Transform
const upper = fruits.map(f => f.toUpperCase());
const long = fruits.filter(f => f.length > 5);
```

---

## Asynchronous JavaScript: Callbacks

**The Problem:**
JavaScript is single-threaded, but operations like network requests take time. We need to handle operations that complete later without blocking execution.

**Callback Pattern:**
```javascript
function fetchData(url, callback) {
    // Simulate network request
    setTimeout(() => {
        const data = {id: 1, name: "Sarah"};
        callback(data);
    }, 1000);
}

// Usage
fetchData("/api/user", (user) => {
    console.log(user.name);  // "Sarah" (after 1 second)
});

console.log("Request sent");  // Prints immediately
```

**Callback Hell (Problem):**
```javascript
fetchUser(id, (user) => {
    fetchPosts(user.id, (posts) => {
        fetchComments(posts[0].id, (comments) => {
            // Deeply nested, hard to read
        });
    });
});
```

---

## Asynchronous JavaScript: Promises

**Promises solve callback hell:**
```javascript
function fetchData(url) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (url) {
                resolve({id: 1, name: "Sarah"});
            } else {
                reject(new Error("Invalid URL"));
            }
        }, 1000);
    });
}

// Chaining promises
fetchData("/api/user")
    .then(user => fetchPosts(user.id))
    .then(posts => fetchComments(posts[0].id))
    .then(comments => console.log(comments))
    .catch(error => console.error(error));
```

**Promise States:**
- **Pending:** Initial state
- **Fulfilled:** Operation completed successfully
- **Rejected:** Operation failed

---

## Asynchronous JavaScript: Async/Await

**Modern syntax (ES2017+):**
```javascript
async function getUserData(id) {
    try {
        const user = await fetchData(`/api/user/${id}`);
        const posts = await fetchPosts(user.id);
        const comments = await fetchComments(posts[0].id);
        return comments;
    } catch (error) {
        console.error("Failed:", error);
        return null;
    }
}

// Usage
const data = await getUserData(1);
```

**Benefits:**
- Looks like synchronous code
- Easier error handling with try/catch
- Better readability and maintainability
- Still non-blocking under the hood

---

## DOM Manipulation

**The Document Object Model (DOM):**
JavaScript's primary use in browsers is manipulating the DOM - the tree structure representing HTML.

**Common DOM Operations:**
```javascript
// Select elements
const button = document.getElementById("myButton");
const items = document.querySelectorAll(".item");

// Modify content
button.textContent = "Click Me";
button.innerHTML = "<strong>Click</strong> Me";

// Modify attributes
button.setAttribute("disabled", true);
button.classList.add("active");

// Create and add elements
const newDiv = document.createElement("div");
newDiv.textContent = "Hello";
document.body.appendChild(newDiv);
```

---

## Event Handling

**Responding to User Actions:**
```javascript
const button = document.getElementById("submitBtn");

// Add event listener
button.addEventListener("click", (event) => {
    console.log("Button clicked!");
    event.preventDefault();  // Prevent default behavior
});

// Common events
element.addEventListener("mouseover", handleHover);
element.addEventListener("keydown", handleKeyPress);
form.addEventListener("submit", handleSubmit);
```

**Event Delegation:**
```javascript
// Handle clicks on any button within container
document.getElementById("container").addEventListener("click", (e) => {
    if (e.target.tagName === "BUTTON") {
        console.log("Button clicked:", e.target.textContent);
    }
});
```

---

## Practical Example: Interactive Web Page

**HTML:**
```html
<input type="text" id="taskInput" placeholder="Enter task">
<button id="addBtn">Add Task</button>
<ul id="taskList"></ul>
```

**JavaScript:**
```javascript
const input = document.getElementById("taskInput");
const button = document.getElementById("addBtn");
const list = document.getElementById("taskList");

button.addEventListener("click", () => {
    const task = input.value.trim();
    if (task) {
        const li = document.createElement("li");
        li.textContent = task;
        list.appendChild(li);
        input.value = "";  // Clear input
    }
});
```

---

## JavaScript Example: Simple Web Server

**Using Node.js (20 lines vs 500+ in C):**
```javascript
const http = require('http');

const server = http.createServer((req, res) => {
    if (req.url === '/') {
        res.writeHead(200, {'Content-Type': 'text/html'});
        res.end('<h1>Hello World</h1>');
    } else if (req.url === '/api/data') {
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({message: 'Hello from API'}));
    } else {
        res.writeHead(404);
        res.end('Not Found');
    }
});

server.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});
```

**What JavaScript handles automatically:**
- Memory management
- String manipulation
- JSON parsing/serialization
- HTTP protocol details

---

## ES6+ Modern JavaScript Features

**Template Literals:**
```javascript
const name = "Sarah";
const age = 25;
const message = `Hello, I'm ${name} and I'm ${age} years old`;
```

**Spread Operator:**
```javascript
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5];  // [1, 2, 3, 4, 5]
const obj2 = {...obj1, newKey: "value"};  // Copy and extend
```

**Default Parameters:**
```javascript
function greet(name = "Guest") {
    return `Hello, ${name}`;
}
```

**Optional Chaining:**
```javascript
const city = user?.address?.city;  // Safe navigation
```

---

## JavaScript Ecosystem

**Package Management:**
- **npm** (Node Package Manager): 2+ million packages
- `package.json` - Project dependencies and scripts
- Install packages: `npm install express`

**Popular Libraries/Frameworks:**
- **React, Vue, Angular** - UI frameworks
- **Express** - Web server framework
- **Lodash** - Utility functions
- **Axios** - HTTP client
- **Jest** - Testing framework

**Build Tools:**
- **Webpack, Vite** - Module bundlers
- **Babel** - JavaScript transpiler
- **ESLint** - Code linter

---

## JavaScript Best Practices

**1. Use const/let instead of var:**
```javascript
const API_URL = "https://api.example.com";  // Won't change
let count = 0;  // Will change
```

**2. Avoid global variables:**
```javascript
// Bad
var userData = {};

// Good
function createApp() {
    const userData = {};
    // userData is scoped to function
}
```

**3. Use strict equality:**
```javascript
// Bad: type coercion
if (x == "5") { }

// Good: strict comparison
if (x === 5) { }
```

---

## JavaScript Best Practices (continued)

**4. Handle errors properly:**
```javascript
async function fetchData() {
    try {
        const response = await fetch(url);
        return await response.json();
    } catch (error) {
        console.error("Failed to fetch:", error);
        return null;
    }
}
```

**5. Use meaningful names:**
```javascript
// Bad
const d = new Date();
const x = users.filter(u => u.a);

// Good
const currentDate = new Date();
const activeUsers = users.filter(user => user.isActive);
```

---

## Common JavaScript Pitfalls

**1. `this` context:**
```javascript
const obj = {
    value: 42,
    getValue: function() {
        return this.value;  // 'this' is obj
    }
};

const fn = obj.getValue;
fn();  // 'this' is undefined/window! Use arrow functions or bind()
```

**2. Truthy/Falsy values:**
```javascript
// Falsy: false, 0, "", null, undefined, NaN
if ("" || 0 || null) {
    // Won't execute
}

// Be explicit when needed
if (count === 0) { }  // Better than if (!count)
```

---

## JavaScript Performance Considerations

**1. Minimize DOM manipulation:**
```javascript
// Bad: 1000 DOM operations
for (let i = 0; i < 1000; i++) {
    list.appendChild(createItem(i));
}

// Good: 1 DOM operation
const fragment = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
    fragment.appendChild(createItem(i));
}
list.appendChild(fragment);
```

**2. Debounce expensive operations:**
```javascript
function debounce(fn, delay) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn(...args), delay);
    };
}

input.addEventListener("input", debounce(search, 300));
```

---

## The Impact of JavaScript on Development

**Productivity Gains:**
- **100x faster development** compared to C for web tasks
- Hours instead of weeks for basic functionality
- Rich ecosystem reduces "reinventing the wheel"

**Challenges JavaScript Introduces:**
- **No type safety** - bugs caught at runtime, not compile time
- **Loose equality** - unexpected type coercion
- **Callback hell** - complex async code (solved by promises/async-await)
- **Growing codebases** - harder to maintain at scale

**This leads us to Week 6:** TypeScript addresses JavaScript's type safety issues while preserving its productivity benefits.

---

## JavaScript in the Modern Web

**JavaScript's Evolution:**
- 1995: Created in 10 days at Netscape
- 1997: ECMAScript standardization
- 2009: Node.js brings JavaScript to servers
- 2015: ES6 modernizes the language
- 2025: Powers most of the web

**Key Takeaways:**
- High-level languages trade control for productivity
- JavaScript makes web development accessible
- Automatic memory management prevents common bugs
- Async programming enables responsive UIs
- Rich ecosystem accelerates development
- Foundation for TypeScript and React (Week 6)

---

<!-- _class: lead -->
