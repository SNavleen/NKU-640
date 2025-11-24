---
marp: true
theme: default
paginate: true
<!-- _class: lead -->
<!-- _paginate: skip -->
# Homework 3: High-Level Programming Languages

Building Todo Apps in JavaScript, TypeScript, and React

---

## HW3: Project Overview

Built three implementations of the same Todo application to demonstrate the evolution and benefits of high-level programming languages:

1. **JavaScript Todo App** – Vanilla JavaScript with DOM manipulation
2. **TypeScript Todo App** – Type-safe version with strict typing
3. **React Todo App** – Component-based architecture with hooks

**Goal:** Understand how high-level languages and frameworks help create high-quality software effectively.

---

## Application Structure Comparison

### JavaScript
```
javascript-todo/
├── app.js              # Business logic and DOM manipulation
└── index.html          # Structure and styles
```

### TypeScript
```
typescript-todo/
├── src/
│   ├── app.ts          # Type-safe source code
│   ├── index.html      # HTML structure
│   └── tsconfig.json   # TypeScript configuration
└── app.js              # Compiled JavaScript
```

### React
```
react-todo/
├── package.json        # Dependencies and build scripts
├── src/
│   ├── App.tsx         # React components with TypeScript
│   └── index.html      # HTML with root div
└── app.js              # Bundled output
```

---

## How High-Level Languages Improve Software Quality

### 1. Abstraction - Focus on "What" Not "How"

**JavaScript (Low-Level DOM Manipulation):**
```javascript
const li = document.createElement('li');
const checkbox = document.createElement('input');
checkbox.type = 'checkbox';
li.appendChild(checkbox);
// ... manual DOM construction
```

**React (High-Level Declarative):**
```tsx
<li className={todo.completed ? 'completed' : ''}>
  <input type="checkbox" checked={todo.completed} />
  <span>{todo.text}</span>
</li>
```

**Benefit:** React abstracts away DOM manipulation, letting developers focus on UI logic rather than implementation details.

---

## 2. Type Safety - Catching Errors Early

**JavaScript (Runtime Errors):**
```javascript
function deleteTodo(id) {
  todos = todos.filter(t => t.id !== id);  // No type checking
}
```

**TypeScript (Compile-Time Safety):**
```typescript
private deleteTodo(id: number): void {
  const todo: Todo | undefined = this.todos.find(
    (t: Todo): boolean => t.id === id
  );
  // TypeScript ensures type correctness
}
```

**Benefit:** TypeScript catches type errors during development, preventing runtime bugs and providing better IDE support.

---

## 3. Component Reusability

**JavaScript (Duplicate Code):**
```javascript
// Must repeat similar logic for each todo item
todos.forEach(todo => {
  const li = document.createElement('li');
  const checkbox = document.createElement('input');
  // ... repeat for every todo
});
```

**React (Reusable Components):**
```tsx
const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggle, onDelete }) => (
  <li className={todo.completed ? 'completed' : ''}>
    <input type="checkbox" onChange={() => onToggle(todo.id)} />
    <span>{todo.text}</span>
    <button onClick={() => onDelete(todo.id)}>Delete</button>
  </li>
);
```

**Benefit:** React components are self-contained, reusable units that eliminate code duplication.

---

## 4. State Management

**JavaScript (Manual State Tracking):**
```javascript
let todos = [];

function addTodo() {
  todos.push(newTodo);
  displayTodos();  // Manually update UI
}
```

**React (Automatic UI Updates):**
```tsx
const [todos, setTodos] = useState<Todo[]>([]);

const addTodo = (text: string): void => {
  setTodos([...todos, newTodo]);  // UI updates automatically
};
```

**Benefit:** React automatically re-renders when state changes, eliminating manual DOM synchronization bugs.

---

## 5. Maintainability & Scalability

### Code Organization Comparison

| Aspect | JavaScript | TypeScript | React |
|--------|-----------|-----------|-------|
| **Structure** | Functions | Classes | Components |
| **Type Safety** | None | Full | Full |
| **Reusability** | Limited | Medium | High |
| **Testing** | Difficult | Easier | Easiest |
| **Team Collaboration** | Hard | Better | Best |
| **Scalability** | Poor | Good | Excellent |

---

## Real-World Impact: Lines of Code

**Same functionality, different complexity:**

- **JavaScript:** ~140 lines of imperative code
- **TypeScript:** ~160 lines (extra type annotations pay off in safety)
- **React:** ~180 lines split into 4 reusable components

**But consider:**
- React code is more maintainable
- TypeScript prevents entire classes of bugs
- Components can be reused across projects

---

## Developer Experience Benefits

### JavaScript
- ❌ No autocomplete for object properties
- ❌ Runtime type errors
- ❌ Manual DOM updates prone to bugs
- ✅ Quick to start, no build step

### TypeScript
- ✅ Full IDE autocomplete and IntelliSense
- ✅ Compile-time error detection
- ✅ Self-documenting interfaces
- ⚠️ Requires build step

### React
- ✅ Component-based thinking
- ✅ Automatic UI updates
- ✅ Rich ecosystem of libraries
- ⚠️ Steeper learning curve

---

## Key Features Implemented

All three apps implement identical functionality:

1. ✅ **Add todos** - Create new todo items
2. ✅ **Toggle completion** - Mark as complete/incomplete
3. ✅ **Delete todos** - Remove individual items (with confirmation for uncompleted)
4. ✅ **Clear completed** - Bulk remove finished tasks
5. ✅ **Clear all** - Delete all todos (with confirmation)
6. ✅ **Persistent storage** (React only) - Uses localStorage

---

## Lessons Learned: Language Evolution

### JavaScript (1995)
- Foundation of web interactivity
- Flexible but error-prone
- Manual everything

### TypeScript (2012)
- JavaScript + Type Safety
- Better tooling and refactoring
- Catches bugs before runtime

### React (2013)
- Declarative UI paradigm
- Component-based architecture
- Modern web development standard

**Each evolution addresses pain points of the previous generation.**

---

## How High-Level Languages Enable Quality Software

### 1. **Faster Development**
- Less boilerplate code
- Built-in patterns and best practices
- Rich ecosystems and libraries

### 2. **Fewer Bugs**
- Type safety catches errors early
- Automatic state management
- Framework handles edge cases

### 3. **Better Collaboration**
- Clear interfaces and contracts
- Self-documenting code
- Shared vocabulary (components, props, state)

### 4. **Easier Maintenance**
- Modular, isolated components
- Safe refactoring with types
- Clear separation of concerns

---

## Practical Application to Course Principles

### APIEC Framework Applied:
- **Abstraction:** React abstracts DOM manipulation
- **Polymorphism:** Components accept different data through props
- **Inheritance:** TypeScript class hierarchy (TodoApp extends base functionality)
- **Encapsulation:** Private class members, component state
- **Composition:** React components composed of smaller components

### SOLID Principles:
- **Single Responsibility:** Each React component has one job
- **Open/Closed:** Components extensible via props
- **Dependency Inversion:** React uses dependency injection via props

---

## Conclusion: Why High-Level Languages Matter

**The Evolution Path:**
1. Machine Code → Assembly → C (increasing abstraction)
2. C → JavaScript (high-level, garbage collected)
3. JavaScript → TypeScript (type safety)
4. TypeScript → React (framework abstractions)

**Each step trades some control for:**
- ✅ Productivity gains
- ✅ Reduced bug rates
- ✅ Better maintainability
- ✅ Easier collaboration

**Result:** High-level languages and frameworks enable developers to build high-quality software more effectively by handling low-level concerns automatically, enforcing best practices, and providing powerful abstractions.

---

## References

