import './App.css';
import React from 'react';

import Jumbotron from 'react-bootstrap/Jumbotron';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import 

class SteamForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: ''};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    alert('wow, such a cool button!');
    event.preventDefault();
  }

  render() {
    return( 
      <>
      <form onSubmit={this.handleSubmit}>
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
