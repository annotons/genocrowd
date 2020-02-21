import React, { Component } from 'react'
import axios from 'axios'
import { Button, Form, FormGroup, Label, Input, Alert, Navbar, Row, Container, Col, Table, Media, Jumbotron} from 'reactstrap'
import { Redirect} from 'react-router-dom'
import ErrorDiv from '../error/error'
import WaitingDiv from '../../components/waiting'
import update from 'react-addons-update'
import PropTypes from 'prop-types'
import Image from 'react-bootstrap/Image'
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
        <Col xs>
          <Image src="../static/logo/2-2-happy-person-free-download-png.png" roundedCircle />
          </Col>
        <Col style={{ height: 20}}> {this.props.config.user.username}</Col>   
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
