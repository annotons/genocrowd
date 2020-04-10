import React, { Component } from 'react'
import axios from 'axios'
import { Container, Card, Col, Row, CardHeader } from 'reactstrap'
import update from 'react-addons-update'
import PropTypes from 'prop-types'
import Iframe from 'react-iframe'
import Start from './start'
import Stop from './stop'
export default class Annotator extends Component {
  constructor (props) {
    super(props)
    this.state = ({
      category: 1,
      answers: {
        startinfo : {
          startfound:'',
          startokpos: '',
          startfoundable:'',
          position: 0,
        },
        stopinfo : {
          stopfound:'',
          stopokpos: '',
          stopfoundable:'',
          position: 0,
        }}
  
  })
    this.nextCategory = this.nextCategory.bind(this)
  }

  nextCategory (newValue) {
    console.log('nextC')
    this.setState({category: newValue})
  }




  componentDidMount () {

    if (!this.props.config.user) {
      axios.post('/api/auth/check')
      .then(Response => {
        console.log(Response)
        this.props.setStateNavbar({
          config: update(this.props.config,{
            user: {$set: Response.data.user},
            logged: {$set: !Response.data.error}
          })
        })
      })
      axios.post('/api/apollo/questionloader')
      .then(Response => {
        console.log(Response)
        this.props.setStateNavbar({
          config: update(this.props.config,{
            user: {$set: Response.data.user},
            logged: {$set: !Response.data.error}
          })
        })

      })
    }

    }

  render () {
    let html
    let questioncategory
    if (this.state.category === 1) {
    questioncategory = <Start config={this.props.config} categoryhandler={this.nextCategory}/>
    }
    else if (this.state.category === 2) {
    questioncategory = <Stop config={this.props.config} categoryhandler={this.nextCategory}/>
      }

    html =  (
        <div>
          <br/>
        <Container>
          <Row>
            <Col>
              <Iframe url="http://localhost:8080/apollo"
                width="900px"
                height="700px"
                display="inline"
                position="relative"/>
            </Col>
            <Col>
              <Card>
                <CardHeader> Questions:</CardHeader>
                {questioncategory}
              </Card>
            </Col>
          </Row>

        </Container>
      </div>
    )
    return html
  }
}


Annotator.propTypes = {
  waitForStart: PropTypes.bool,
  config: PropTypes.object,
  setStateNavbar: PropTypes.func
}

