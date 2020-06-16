import React, { Component } from 'react'
import axios from 'axios'
import { Card, Col, Row, CardHeader, Button, CardBody, ListGroup, ListGroupItem } from 'reactstrap'
import { Accordion } from 'react-bootstrap'
import update from 'react-addons-update'
import { Redirect } from 'react-router'
import PropTypes from 'prop-types'
import Iframe from 'react-iframe'
export default class Annotator extends Component {
  constructor (props) {
    super(props)
    this.state = ({
      category: 1,
      
      url: "",
      sequenceName: "",
      finished: false
  })
    this.nextCategory = this.nextCategory.bind(this)
    this.setFinish = this.setFinish.bind(this)
  }

  nextCategory (newValue) {
    console.log('nextC')
    this.setState({category: newValue})
  }

  setFinish () {
    let requestUrl = 'api/apollo/save'
    let data = {sequence: this.state.sequenceName}
    axios.post(requestUrl, data , { baseURL: this.props.config.proxyPath, cancelToken: new axios.CancelToken((c) => { this.cancelRequest = c }) })
      .then(response => {
        console.log(requestUrl, response.data)
        this.setState({
          error: response.data.error,
          errorMessage: response.data.errorMessage,
          status: response.status,
          Redirect: true
        })
          })
        
        this.setState({
          finished: true
        })
      .catch(error => {
        console.log(error)
        this.setState({
          error: true,
          errorMessage: error.response.data.errorMessage,
          status: error.response.status,
          success: !response.data.error,
        })
      })
    event.preventDefault()

  }


  componentDidMount () {
    console.log(this.state.url)
    if (!this.props.config.user) {
      axios.post('/api/auth/check')
      .then(Response => {
        console.log(Response)
        this.props.setStateNavbar({
          config: update(this.props.config,{
            user: {$set: Response.data},
            logged: {$set: !Response.data.error}
          })
        })
      })
      
    }
    axios.get('/api/apollo/genechoice')
      .then(Response => {
        console.log(Response)
        this.setState({
          url: Response.data.url,
          sequenceName: Response.data.attributes
        })

      })
      console.log(this.state.url)
    }

  render () {
    let html = <Redirect to="/dashboard" />
    if (this.state.finished === false) {
      html =  (
        <div className="annotator">
          <br/>

        {/* <Container > */}
          <Row>
            <Col>
              <Iframe url={this.state.url}
                width="900px"
                height="700px"
                display="inline"
                position="relative"/>
            </Col>
            <Col>
              <Card>
                <CardHeader> Questions about:</CardHeader>
                {/* {questioncategory} */}
                <Accordion defaultActiveKey="0">
                  <Card>
                    <Accordion.Toggle as={CardHeader} eventKey="0">
                      Start and Stop codons
                    </Accordion.Toggle>
                    <Accordion.Collapse eventKey="0">
                      <CardBody>
                      <ListGroup>
                        <ListGroupItem>Is the Start codon found?</ListGroupItem>
                        <ListGroupItem>If so it at the right place?</ListGroupItem>
                        <ListGroupItem>Else can you find it?</ListGroupItem>
                        <ListGroupItem>Is the Stop codon found?</ListGroupItem>
                        <ListGroupItem>If so it at the right place?</ListGroupItem>
                        <ListGroupItem>Else can you find it?</ListGroupItem>
                      </ListGroup>
                      </CardBody>
                    </Accordion.Collapse>
                  </Card>
                  <Card>
                    <Accordion.Toggle as={CardHeader} eventKey="1">
                      5&apos; and 3&apos; UTR
                    </Accordion.Toggle>
                    <Accordion.Collapse eventKey="1">
                      <CardBody>Hello! I m another body</CardBody>
                    </Accordion.Collapse>
                  </Card>
                  <Card>
                    <Accordion.Toggle as={CardHeader} eventKey="2">
                      Introns and Exons
                    </Accordion.Toggle>
                    <Accordion.Collapse eventKey="2">
                      <CardBody>Hello! I m another body</CardBody>
                    </Accordion.Collapse>
                  </Card>
                </Accordion>
                <Button color="success" onClick={this.setFinish}>Save results</Button>
              </Card>
            </Col>
          </Row>
  
        {/* </Container> */}
      </div>
    )
    }
    
    return html
  }
}


Annotator.propTypes = {
  waitForStart: PropTypes.bool,
  config: PropTypes.object,
  setStateNavbar: PropTypes.func
}

