import React, { Component } from 'react'
import axios from 'axios'
import { FormGroup, Label, Input, Col } from 'reactstrap'
import PropTypes from 'prop-types'
import Utils from '../../classes/utils'

export default class Users extends Component {
  constructor (props) {
    super(props)
    this.utils = new Utils()
    this.state = { isLoading: true,
      error: false,
      errorMessage: '',
      users: [],
      chrselect1: false,
      chrselect2: false
    }
    
    
    this.cancelRequest
  }

  componentDidMount () {
    if (!this.props.waitForStart) {
      let requestUrl = '/api/admin/getusers'

      axios.get(requestUrl, { baseURL: this.props.config.proxyPath, cancelToken: new axios.CancelToken((c) => { this.cancelRequest = c }) })
        .then(response => {
          console.log(requestUrl, response.data)
          this.setState({
            isLoading: false,
            error: response.data.error,
            errorMessage: response.data.errorMessage,
            users: response.data.users
          })
        })
        .catch(error => {
          console.log(error, error.response.data.errorMessage)
          this.setState({
            error: true,
            errorMessage: error.response.data.errorMessage,
            status: error.response.status,
            success: !response.data.error
          })
        })
    }
  }



  componentWillUnmount () {
    if (!this.props.waitForStart) {
      this.cancelRequest()
    }
  }

  render () {

    return (
      <div className="container">
        <h2>Question management</h2>
        <hr />
        <div>
        <FormGroup>
        <Col>
        <Label for="chromosomeSelect">Chromosome</Label>
        <Input type="select" name="select" id="chromosomeSelect">
          <option>CH1</option>
          <option>CH2</option>
          <option>CH3</option>
          <option>CH4</option>
          <option>CH5</option>
        </Input>
        </Col>
        <Col>
        <Label for="positionSelect">Position</Label>
        <Input type="select" name="select" id="positionSelect">
          <option>100</option>
          <option>200</option>
          <option>300</option>
          <option>400</option>
          <option>500</option>
        </Input>
        </Col>
      </FormGroup>
  </div>
        <div className=".geno-table-height-div">
          
        </div>
      </div>
    )
  }
}

Users.propTypes = {
  waitForStart: PropTypes.bool,
  config: PropTypes.object
}