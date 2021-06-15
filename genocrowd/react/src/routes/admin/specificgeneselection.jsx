import React, { Component } from "react";
import axios from "axios";
import { Label, Input, Button } from "reactstrap";
import PropTypes from "prop-types";
import Utils from "../../classes/utils";

export default class SpecificGeneSelection extends Component {
  constructor(props) {
    super(props);
    this.utils = new Utils();
    this.state = {
      isLoading: true,
      error: false,
      errorMessage: "",
      selectedFile: null,
      priority:0,
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.onChangeHandler = this.onChangeHandler.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.cancelRequest;
  }

  handleSubmit(event) {
    let requestUrl = "/api/data/uploadgenes";
    const data = new FormData();
    data.append("file", this.state.selectedFile);
    data.append("priority", this.state.priority);

    axios
      .post(requestUrl, data, {
        baseURL: this.props.config.proxyPath,
        cancelToken: new axios.CancelToken((c) => {
          this.cancelRequest = c;
        }),
      })
      .then((response) => {
        console.log(requestUrl, response.data);
        console.log(response.data.errorMessage);
        this.setState({
          error: response.data.error,
          errorMessage: response.data.errorMessage,
        });
      })
      .catch((error) => {
        console.log(error, error.response.data.errorMessage);
        this.setState({
          error: true,
          errorMessage: error.response.data.errorMessage,
          status: error.response.status,
        });
      });
    event.preventDefault();
  }

  onChangeHandler(e) {
    this.setState({
      selectedFile: e.target.files[0],
    });
  }

  handleChange(event){
    event.preventDefault();
    this.setState({
      [event.target.id]: event.target.value
    })
  }

  render() {
    return (
      <div className="container">
        <div className=".geno-table-height-div">
          <h2>Import a new gene to annotate</h2>
          <Label for="exampleFile">File</Label>
          <Input
            type="file"
            name="file"
            id="exampleFile"
            onChange={(e)=> this.onChangeHandler(e)}
          />
          <Input 
            type="number"
            name="priority"
            id="priority"
            onChange = {(e)=> this.handleChange(e)}
          />
          <br></br>
          Import the GFF file associated to the gene you wish to annotate:
          <Button
            disabled={!this.state.selectedFile}
            onClick={this.handleSubmit}
          >
            Upload
          </Button>
        </div>
        <hr />
        <hr />
      </div>
    );
  }
}

SpecificGeneSelection.propTypes = {
  waitForStart: PropTypes.bool,
  config: PropTypes.object,
};
