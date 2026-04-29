import { useState, useEffect } from 'react';
import axios from 'axios';
import { PlusCircle, CheckCircle2, Circle, Trash2, ListTodo } from 'lucide-react';

const API_URL = 'http://localhost:8000/todos';

function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Fetch all todos on mount
  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const response = await axios.get(API_URL);
      setTodos(response.data);
    } catch (error) {
      console.error('Error fetching todos:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !description.trim()) return;

    setIsLoading(true);
    try {
      const newTodo = {
        id: Date.now(), // Generate a simple ID
        title,
        description,
        status: false
      };
      await axios.post(API_URL, newTodo);
      setTitle('');
      setDescription('');
      fetchTodos();
    } catch (error) {
      console.error('Error creating todo:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleStatus = async (todo) => {
    try {
      const updatedTodo = { ...todo, status: !todo.status };
      await axios.put(`${API_URL}/${todo.id}`, updatedTodo);
      fetchTodos();
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  };

  const deleteTodo = async (id) => {
    try {
      await axios.delete(`${API_URL}/${id}`);
      fetchTodos();
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Task Manager</h1>
        <p>Stay organized, focused, and get things done.</p>
      </header>

      <form onSubmit={handleSubmit} className="todo-form">
        <div className="input-group">
          <input
            type="text"
            placeholder="What needs to be done?"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            disabled={isLoading}
          />
        </div>
        <div className="input-group">
          <textarea
            placeholder="Add some details..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={isLoading}
          />
        </div>
        <button type="submit" className="btn-submit" disabled={isLoading || !title.trim()}>
          <PlusCircle size={20} />
          {isLoading ? 'Adding...' : 'Add Task'}
        </button>
      </form>

      <div className="todo-list">
        {todos.length === 0 ? (
          <div className="empty-state">
            <ListTodo className="empty-icon" />
            <p>No tasks yet. Add one above to get started!</p>
          </div>
        ) : (
          todos.map((todo) => (
            <div key={todo.id} className={`todo-item ${todo.status ? 'completed' : ''}`}>
              <div className="todo-content">
                <h3 className={`todo-title ${todo.status ? 'completed' : ''}`}>
                  {todo.title}
                </h3>
                <p className="todo-desc">{todo.description}</p>
              </div>
              <div className="todo-actions">
                <button
                  className="btn-icon success"
                  onClick={() => toggleStatus(todo)}
                  title={todo.status ? "Mark incomplete" : "Mark complete"}
                >
                  {todo.status ? <CheckCircle2 size={24} /> : <Circle size={24} />}
                </button>
                <button
                  className="btn-icon danger"
                  onClick={() => deleteTodo(todo.id)}
                  title="Delete task"
                >
                  <Trash2 size={24} />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
