import React, { Component } from 'react'
import axios from 'axios'
import {Button, CardImg, CardText, CardBody,
  CardTitle, CardSubtitle ,Form, FormGroup, Label, Input, Alert, Navbar, Spinner,Row, Container, Col, Table, Media, Jumbotron, Card} from 'reactstrap'
import { Redirect} from 'react-router-dom'
import ErrorDiv from '../error/error'
import WaitingDiv from '../../components/waiting'
import update from 'react-addons-update'
import PropTypes from 'prop-types'
import Image from 'react-bootstrap/Image'
import Identicon from 'react-identicons';
export default class Dashboard extends Component {
  constructor (props) {
    super(props)
  }
  
  render () {
    const imgStyle = {
      maxHeight: 64,
      maxWidth: 64
    }
    let html = (
      <Container>
      <Row>
        
        <Col width={50} xs>
          <Card width= {50} body outline color="secondary">
            <CardBody className="text-center tile">
              <Identicon size={100} string={this.props.config.user.username}/>
            </CardBody>
            
          </Card>
        </Col>
        <Col width={50} xs> 
          <Card body outline color="secondary">
            <CardBody className="text-center tile ">
              {this.props.config.user.username}            
            </CardBody>
          </Card>
        </Col>   
      </Row>
      
      <Row>
      <Jumbotron fluid >
        <Container fluid>
          <h1 className="display-4">Statistics</h1>
          <h2 className="display-5">Number of Annotated genes</h2>
          <p className="lead">57</p>
        </Container>
      </Jumbotron>
        
      </Row>
      <Row>
        <Col>
        <Table hover>
            <thead>
              <tr>
                <th>Twitter feed</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>dude1: Best tool ever #genocrowd</td>
              </tr>
              <tr>
                <td>dude2: The future of annotation tools! #genocrowd</td>
                
              </tr>
              <tr>
                <td>etc...</td>

              </tr>
            </tbody>
          </Table>
        
        </Col>
        <Col>
          <Jumbotron>
            <h1 className="display-3">Hello</h1>
            <p className="lead">You can now Annotate!</p>
            <hr className="my-2" />
            <Button color="success">Get Started</Button>{' '}
          </Jumbotron>
        </Col>
        <Col>
          <Table hover>
            <thead>
              <tr>
                <th colSpan="2">Top Annotators</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1</td>
                <td>Me</td>
              </tr>
              <tr>
                <td>2</td>
                <td>Myself</td>
              </tr>
              <tr>
                <td>3</td>
                <td>I</td>
              </tr>
            </tbody>
          </Table>
        </Col>
      </Row>
    </Container>
    )
    // if(!this.props.config.logged){
        
    //   return <Redirect to='/login'/>;
    // }
    return html
  }
}
Dashboard.propTypes = {
  config: PropTypes.object
}