import React, { useState, useEffect } from 'react';
import { Container, Typography, TextField, Button, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton } from '@material-ui/core';
import { Delete, Edit } from '@material-ui/icons';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [topics, setTopics] = useState([]);
  const [newTopic, setNewTopic] = useState({ title: '', content: '', tags: '' });
  const [editingTopic, setEditingTopic] = useState(null);

  useEffect(() => {
    fetchTopics();
  }, []);

  const fetchTopics = async () => {
    const response = await axios.get(`${API_URL}/topics`);
    setTopics(response.data);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (editingTopic) {
      setEditingTopic({ ...editingTopic, [name]: value });
    } else {
      setNewTopic({ ...newTopic, [name]: value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (editingTopic) {
      await axios.put(`${API_URL}/topics/${editingTopic.id}`, {
        ...editingTopic,
        tags: editingTopic.tags.split(',').map(tag => tag.trim())
      });
      setEditingTopic(null);
    } else {
      await axios.post(`${API_URL}/topics`, {
        ...newTopic,
        tags: newTopic.tags.split(',').map(tag => tag.trim())
      });
      setNewTopic({ title: '', content: '', tags: '' });
    }
    fetchTopics();
  };

  const handleEdit = (topic) => {
    setEditingTopic({ ...topic, tags: topic.tags.join(', ') });
  };

  const handleDelete = async (id) => {
    await axios.delete(`${API_URL}/topics/${id}`);
    fetchTopics();
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h2" component="h1" gutterBottom>
        Causal Inference Knowledge Base
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          fullWidth
          margin="normal"
          name="title"
          label="Topic Title"
          value={editingTopic ? editingTopic.title : newTopic.title}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          margin="normal"
          name="content"
          label="Content"
          multiline
          rows={4}
          value={editingTopic ? editingTopic.content : newTopic.content}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          margin="normal"
          name="tags"
          label="Tags (comma-separated)"
          value={editingTopic ? editingTopic.tags : newTopic.tags}
          onChange={handleInputChange}
        />
        <Button type="submit" variant="contained" color="primary">
          {editingTopic ? 'Update Topic' : 'Add Topic'}
        </Button>
      </form>
      <List>
        {topics.map((topic) => (
          <ListItem key={topic.id}>
            <ListItemText
              primary={topic.title}
              secondary={`${topic.content.substring(0, 100)}... | Tags: ${topic.tags.join(', ')}`}
            />
            <ListItemSecondaryAction>
              <IconButton edge="end" aria-label="edit" onClick={() => handleEdit(topic)}>
                <Edit />
              </IconButton>
              <IconButton edge="end" aria-label="delete" onClick={() => handleDelete(topic.id)}>
                <Delete />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>
    </Container>
  );
}

export default App;