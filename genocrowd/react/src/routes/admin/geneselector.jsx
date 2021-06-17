import React, { Component } from "react";
import axios from "axios";
import { FormGroup, CustomInput, Button } from "reactstrap";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";
import cellEditFactory from "react-bootstrap-table2-editor";
import update from "react-addons-update";
import PropTypes from "prop-types";
import Utils from "../../classes/utils";
export default class GeneBoard extends Component {
  constructor(props) {
    super(props);
    this.utils = new Utils();
    this.state = { isLoading: true, error: false, errorMessage: "", genes: [] };
    this.handleChangeAnnotable = this.handleChangeAnnotable.bind(this);
    this.handleRemoveGene = this.handleRemoveGene.bind(this);
    this.handleRemoveAllGenes = this.handleRemoveAllGenes.bind(this);
    this.cancelRequest;
  }

  handleChangeAnnotable(event) {
    let geneT = event.target.getAttribute("gene");
    console.log(geneT)
    let index = this.state.genes.findIndex((gene) => gene._id == geneT);

    let newstatus = 0;
    console.log(event.target.value)
    if (event.target.value == 0) {
      newstatus = 1;
    }

    let requestUrl = "/api/data/setannotable";
    let data = {
      gene: geneT,
      newstatus: newstatus,
    };

    axios
      .post(requestUrl, data, {
        baseURL: this.props.config.proxyPath,
        cancelToken: new axios.CancelToken((c) => {
          this.cancelRequest = c;
        }),
      })
      .then((response) => {
        console.log(requestUrl, response.data);
        console.log(this.state.genes[index])
        this.setState({
          error: response.data.error,
          errorMessage: response.data.errorMessage,
          success: !response.data.error,
          genes: update(this.state.genes, {
            [index]: { isAnnotable: { $set: newstatus } },
          }),
        });
        console.log(this.state.genes[index])

      })
      .catch((error) => {
        console.log(error, error.response.data.errorMessage);
        this.setState({
          error: true,
          errorMessage: error.response.data.errorMessage,
          status: error.response.status,
          success: !response.data.error,
        });
      });
  }

  handleRemoveGene(event) {
    let gene = event.target.getAttribute("gene");
    let requestUrl = "/api/data/removegene";
    let data = {
      _id: gene,
    };

    axios
      .post(requestUrl, data, {
        baseURL: this.props.config.proxyPath,
        cancelToken: new axios.CancelToken((c) => {
          this.cancelRequest = c;
        }),
      })
      .then((response) => {
        console.log(requestUrl, response.data);
        let gene_list = this.state.genes;
        for( var i = 0; i < gene_list.length; i++){ if ( gene_list[i]["_id"] === gene) { gene_list.splice(i, 1); }}
        this.setState({
          error: response.data.error,
          errorMessage: response.data.errorMessage,
          success: !response.data.error,
          genes: gene_list,
        });
      })
      .catch((error) => {
        console.log(error, error.response.data.errorMessage);
        this.setState({
          error: true,
          errorMessage: error.response.data.errorMessage,
          status: error.response.status,
          success: !response.data.error,
        });
      });
  }

  handleRemoveAllGenes(){
    let requestUrl = "api/data/removeallgenes";

    axios
      .get(requestUrl, {
        baseURL: this.props.config.proxyPath,
        cancelToken: new axios.CancelToken((c) => {
          this.cancelRequest = c;
        }),
      })
      .then((response) => {
        console.log(requestUrl, response.data);
      })
  }

  componentDidMount() {
    if (!this.props.waitForStart) {
      let requestUrl = "/api/data/getgenes";
      console.log("mounting");
      axios
        .get(requestUrl, {
          baseURL: this.props.config.proxyPath,
          cancelToken: new axios.CancelToken((c) => {
            this.cancelRequest = c;
          }),
        })
        .then((response) => {
          console.log(requestUrl, response.data);
          this.setState({
            isLoading: false,
            error: response.data.error,
            errorMessage: response.data.errorMessage,
            genes: response.data.genes,
          });
        })
        .catch((error) => {
          console.log(error, error.response.data.errorMessage);
          this.setState({
            error: true,
            errorMessage: error.response.data.errorMessage,
            status: error.response.status,
            success: !response.data.error,
          });
        });
    }
  }

  componentWillUnmount() {
    if (!this.props.waitForStart) {
      this.cancelRequest();
    }
  }

  render() {
    let columns = [
      {
        editable: false,
        dataField: "chromosome",
        text: "Chromosome",
        sort: true,
      },
      {
        editable: false,
        dataField: "_id",
        text: "Gene",
        sort: true,
      },
      {
        editable: false,
        dataField: "isAnnotable",
        text: "Annotable",
        formatter: (cell, row) => {
          return (
            <FormGroup>
              <div>
                <CustomInput
                  type="switch"
                  gene={row._id}
                  id={"set-annotable-" + row._id}
                  name="isAnnotable"
                  onChange={this.handleChangeAnnotable}
                  label="Annotable"
                  checked={cell}
                  value={cell}
                />
              </div>
            </FormGroup>
          );
        },
        sort: true,
      },
      {
        editable: false,
        text: "Remove",
        formatter: (cell, row) => {
          return (
            <FormGroup>
              <div>
                <Button
                  color="danger"
                  name="remove"
                  label="removeButton"
                  gene={row._id}
                  onClick={this.handleRemoveGene}
                >Remove</Button>
              </div>
            </FormGroup>
          );
        },
        sort: true,
      },
      {
        dataField: "uploadDate",
        text: "Added",
        formatter: (cell) => {
          return cell === 0 ? "Unlimited" : cell;
        },
        sort: true,
      },
    ];

    let defaultSorted = [
      {
        dataField: "created",
        order: "asc",
      },
    ];

    return (
      <div className="container">
        <h2>Gene management</h2>
        <hr />
        <div className=".geno-table-height-div">
          <FormGroup>
              <div>
                <Button
                  color="danger"
                  name="remove_all"
                  label="removeAll"
                  onClick={() => window.confirm("Are you sure you wish to delete this item?") && this.handleRemoveAllGenes() }
                >Remove All</Button>
              </div>
            </FormGroup>
          <BootstrapTable
            classes="geno-table"
            wrapperClasses="geno-table-wrapper"
            bootstrap4
            keyField="_id"
            data={this.state.genes}
            columns={columns}
            defaultSorted={defaultSorted}
            pagination={paginationFactory()}
            cellEdit={cellEditFactory({
              mode: "click",
              autoSelectText: true,
            })}
          />
        </div>
      </div>
    );
  }
}

GeneBoard.propTypes = {
  waitForStart: PropTypes.bool,
  config: PropTypes.object,
};
