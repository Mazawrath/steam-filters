import './App.css';
import React from 'react';

import Jumbotron from 'react-bootstrap/Jumbotron';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form'

class SteamForm extends React.Component {
  handleSubmit(event) {
    const formData = new FormData(event.target),
    formDataObj = Object.fromEntries(formData.entries())
    console.log(formDataObj)

    alert('wow, such a cool button!' + formDataObj.steamId);
    event.preventDefault();
  }

  onInput(event) {
    alert("Cool letter! " +  event.target.value);
  }

  render() {
    return( 
      <>
      <form onSubmit={this.handleSubmit}>
      <Form.Group className="mb-3" controlId="formBasicEmail">
      <Form.Label>Steam Vanity URL</Form.Label>
      {/* <Form.Control type="text" placeholder="Enter your Steam vanity URL" onChange={this.onInput} /> */}
      <Form.Control type="text" placeholder="Enter your Steam vanity URL" name="steamId" />
      {/* <Form.Text className="text-muted">
        Insert cool things to say here
      </Form.Text> */}
    </Form.Group>
        <Button type='submit'>Nice button!</Button>
      </form>
      </>
    )
  }
}

function App() {
  return (
    <Container className="p-3">
      <Jumbotron>
      <SteamForm></SteamForm>
      </Jumbotron>
    </Container>
  );
}

export default App;
