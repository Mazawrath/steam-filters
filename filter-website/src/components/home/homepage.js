import React, { useState } from 'react';

import Jumbotron from 'react-bootstrap/Jumbotron';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert'

import GraphicDeisgn from '../../assests/graphicdesign.jpg'

function AlertDismissibleExample() {
    return (
      <Alert variant="danger" >
        <Alert.Heading>User not found!</Alert.Heading>
        <p>
          One or more Steam users were not found! Please double check the marked fields.
        </p>
      </Alert>
    );
}

const Row = function() {
  return <Form.Control type="text" placeholder="Enter your Steam vanity URL" id={"steamId"} onChange={() => this.onInput()} />
}

class SteamForm extends React.Component {
  state = {
    numChildren: 0
  }

  Row = function() {
    return <Form.Control type="text" placeholder="Enter your Steam vanity URL" id={"steamId"} onChange={() => this.onInput() } required isInvalid />
  }

  handleSubmit(event) {
    const formData = new FormData(event.target),
    formDataObj = Object.fromEntries(formData.entries())
    console.log(formDataObj)

    alert('wow, such a cool button!' + formDataObj.steamId);
    event.preventDefault();
  }

  // onInput(event) {
  //   alert("Cool letter! ");
  //   this.setState({
  //     numChildren: this.state.numChildren + 1
  //   });
  // }

  addChild() {
    this.setState({
      numChildren: this.state.numChildren + 1
    });
  }

  render() {
    const steamIdFields = []

    for (var i = 0; i < this.state.numChildren; i++) {
      steamIdFields.push(<Row key={i}/>);
    };

    return( 
      <>
      <form onSubmit={this.handleSubmit}>
      <Form.Group className="mb-3" controlId="formBasicEmail">
      <Form.Label>Steam Vanity URL</Form.Label>
      {/* <Form.Control type="text" placeholder="Enter your Steam vanity URL" id={"steamId"} onChange={() => this.onInput()} /> */}
      <Form.Control type="text" placeholder="Enter your Steam vanity URL" id={"steamId1"} />
      <Form.Control type="text" placeholder="Enter your Steam vanity URL" id={"steamId2"} />
      <Form.Control type="text" placeholder="Enter your Steam vanity URL" id={"steamId3"} />
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
            <AlertDismissibleExample></AlertDismissibleExample>
        <SteamForm></SteamForm>
        </Jumbotron>
        </Container>
        <marquee direction="right" scrolldelay="60"><img src={GraphicDeisgn} height="300"></img></marquee>
    </div>
  );
}