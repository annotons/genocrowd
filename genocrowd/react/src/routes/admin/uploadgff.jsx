import React, { Component } from "react";
import axios from "axios";
import { Label, Input, Button } from "reactstrap";
import PropTypes from "prop-types";
import Utils from "../../classes/utils";

export default class GffUpload extends Component {
  constructor(props) {
    super(props);
    this.utils = new Utils();
    this.state = {
      isLoading: true,
      error: false,
      errorMessage: "",
      selectedFile: null,
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.onChangeHandler = this.onChangeHandler.bind(this);
    this.cancelRequest;
  }

  handleSubmit(event) {
    let requestUrl = "/api/data/selectedgenes";
    const data = new FormData();
    data.append("file", this.state.selectedFile);

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

  componentWillUnmount() {
    if (!this.props.waitForStart) {
      this.cancelRequest();
    }
  }

  render() {
    return (
      <div className="container">
        <div className=".geno-table-height-div">
          <h2>Import a new GFF file</h2>
          <Label for="exampleFile">File</Label>
          <Input
            type="file"
            name="file"
            id="exampleFile"
            onChange={(e) => this.onChangeHandler(e)}
          />
          <br></br>
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

GffUpload.propTypes = {
  waitForStart: PropTypes.bool,
  config: PropTypes.object,
};
