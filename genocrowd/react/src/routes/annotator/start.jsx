import React, { Component } from 'react'
import { Button, ListGroup, Label, ListGroupItem, Input} from 'reactstrap'
import PropTypes from 'prop-types'
import Utils from '../../classes/utils'

export default class Start extends Component {
  constructor (props) {
    super(props)
    this.utils = new Utils()
    this.state = { isLoading: true,
      error: false,
      errorMessage: '',
      fadeIn: false,
      Step: 1,
      startinfo : { startfound:'',
        startokpos: '',
        startfoundable:'',
        NewPosition: 0,
        }
      }
    this.toStep = this.toStep.bind(this)
    this.setStarttoFound = this.setStartFound.bind(this)

  }

  setStartFound (choice) {
    this.setState({
      startinfo: update(startinfo,{
        startfound: {$set: choice}
      })

     })
  }

  setStartokPos (choice) {
    this.setState({
      startinfo: update(startinfo,{
        startfound: {$set: choice}
      })
     })

  }

  toStep (nextStep) {
    this.setState({Step: nextStep})
  }

  renderQ1 () {
    return (
      <div>
        <ListGroup>
            <ListGroupItem>
              <Label>Is the Start Codon present?</Label>
              <Button color="success" onClick={() => {this.setStartFound(true); this.toStep(2)}}>Yes</Button>{' '}
              <Button color="danger" onClick={() => {this.setStartFound(false); this.toStep(3)}}>No</Button>{' '}
            </ListGroupItem>
        </ListGroup>
      </div>
    )
  }

  renderQ2 () {
    return (
      <div>
        <ListGroup>
            <ListGroupItem>
              <Label>Is is at the right coordinates?</Label>
              <Button color="success" onClick={() => {this.setStartokPos(true); this.props.categoryhandler(2)}}>Yes</Button>{' '}
              <Button color="danger" onClick={() => {this.toStep(4)}}>No</Button>{' '}
            </ListGroupItem>
        </ListGroup>
      </div>
    )
  }

  renderQ3 () {
    return (
      <div>
        <ListGroup>
            <ListGroupItem>
              <Label>Can you find it</Label>
              <Button color="success" onClick={() => {this.toStep(4)}}>Yes</Button>{' '}
              <Button color="danger" onClick={() => {this.props.categoryhandler(2)}}>No</Button>{' '}
            </ListGroupItem>
        </ListGroup>
      </div>
    )
    }

  renderQ4 () {
    return (
      <div>
        <ListGroup>
          <ListGroupItem>
            <Label>Enter the right coordinates</Label>
          </ListGroupItem>
        <ListGroupItem>
          <Input></Input>
          <Button onClick={() => {this.props.categoryhandler(2)}}>Validate</Button>
        </ListGroupItem>
        </ListGroup>
      </div>
    )
  }

  render () {
    if (this.state.Step === 1) {
      return( this.renderQ1())
    }
    else if (this.state.Step === 2) {
      return( this.renderQ2())
    }
    else if (this.state.Step === 3) {
      return( this.renderQ3())
    }
    else if (this.state.Step === 4) {
      return( this.renderQ4())
    }
  }
}

Start.propTypes = {
  waitForStart: PropTypes.bool,
  config: PropTypes.object,
  categoryhandler: PropTypes.func,
}