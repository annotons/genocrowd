import React, { Component } from 'react'
import axios from 'axios'
import { Container, Card, Col, Row, CardHeader, Button } from 'reactstrap'
import update from 'react-addons-update'
import { Redirect } from 'react-router'
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
        }},
      url: "",
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
    this.setState({
      finished: true
    })

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
          url: Response.data
        })

      })
      console.log(this.state.url)
    }

  render () {
    let html = <Redirect to="/dashboard" />
    let questioncategory
    if (this.state.category === 1) {
    questioncategory = <Start config={this.props.config} categoryhandler={this.nextCategory}/>
    }
    else if (this.state.category === 2) {
    questioncategory = <Stop config={this.props.config} categoryhandler={this.nextCategory}/>
      }
    if (this.state.finished === false) {
      html =  (
        <div>
          <br/>
        <Container>
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
                <CardHeader> Questions:</CardHeader>
                {questioncategory}
                <Button color="success" onClick={this.setFinish}>Save results</Button>
              </Card>
            </Col>
          </Row>
  
        </Container>
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

