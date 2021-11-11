import React, { useState } from 'react';

import Jumbotron from 'react-bootstrap/Jumbotron';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert'

import GraphicDeisgn from '../../assests/graphicdesign.jpg'

function AlertDismissibleExample(props) {
  const isError = props.isError;

  if (isError) {
    return (
        <Alert variant="danger" >
          <Alert.Heading>User not found!</Alert.Heading>
          <p>
            One or more Steam users were not found! Please double check the marked fields.
          </p>
        </Alert>
    );
  }
  else {
    return <> </>
  }
}

class SteamForm extends React.Component {
  state = {
    numChildren: 1,
    isError: false
  }

  handleSubmit(event) {
    const formData = new FormData(event.target),
    formDataObj = Object.fromEntries(formData.entries())

    this.setState({
      isError: true
    });

    alert('wow, such a cool button!' + formDataObj.steamId_1);
    event.preventDefault();

    this.props.history.push('/thank-you');
  }

  onInput(event) {
    var field_text = event.target.value
    
    if (field_text.length === 1) {
      this.setState({
        numChildren: this.state.numChildren + 1
      });
    } else if (field_text.length === 0) {
      this.setState({
        numChildren: this.state.numChildren - 1
      });
    }
  }

  addChild() {
    this.setState({
      numChildren: this.state.numChildren + 1
    });
  }

  render() {
    const steamIdFields = []

    for (var i = 0; i < this.state.numChildren; i++) {
      steamIdFields.push(<Form.Control rol type="text" placeholder="Enter your Steam vanity URL" name={"steamId_" + i} onChange={(event) => this.onInput(event)} key={i} />);
    };

    return( 
      <>
      <AlertDismissibleExample isError={this.state.isError} />
      <form onSubmit={() => this.handleSubmit(this)}>
      <Form.Group className="mb-3" controlId="formBasicEmail">
      <Form.Label>Steam Vanity URL</Form.Label>
      {steamIdFields}
    </Form.Group>
        <Button type='submit'>Nice button!</Button>
        <Button type='button' onClick={() => this.addChild()}>Add friend</Button>
      </form>
      </>
    );
  }
}



export default function Home() {
  return (
    <div className="wrapper">
        <Container className="p-3">
        <Jumbotron>
          <h1>Enter your Steam vanity URL and your friends vanity URLs</h1>
        <SteamForm></SteamForm>
        </Jumbotron>
        </Container>
        <marquee direction="right" scrolldelay="60"><img src={GraphicDeisgn} height="300" /></marquee>
    </div>
  );
}
