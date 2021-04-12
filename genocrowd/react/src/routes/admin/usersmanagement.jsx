import React, { Component } from "react";
import axios from "axios";
import { FormGroup, CustomInput, Form, Button, Label, Input } from "reactstrap";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";
import cellEditFactory from "react-bootstrap-table2-editor";
import update from "react-addons-update";
import PropTypes from "prop-types";
import Utils from "../../classes/utils";

export default class Users extends Component {
  constructor(props) {
    super(props);
    this.utils = new Utils();
    this.state = { 
      isLoading: true, 
      error: false, 
      errorMessage: "", 
      users: [], 
      newNumber: ""
    }
    this.handleChangeAdmin = this.handleChangeAdmin.bind(this);
    this.handleChangeBlocked = this.handleChangeBlocked.bind(this);
    this.handleChange = this.handleChange.bind(this)
    this.cancelRequest
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleChangeAdmin(event) {
    let username = event.target.getAttribute("username");
    console.log(event.target)
    let index = this.state.users.findIndex((user) => user.username == username);

    let newAdmin = 0;
    if (event.target.value == 0) {
      newAdmin = 1;
    }

    let requestUrl = "/api/admin/setadmin";
    let data = {
      username: username,
      newAdmin: newAdmin,
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
        this.setState({
          error: response.data.error,
          errorMessage: response.data.errorMessage,
          success: !response.data.error,
          users: update(this.state.users, {
            [index]: { isAdmin: { $set: newAdmin } },
          }),
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

  handleChangeBlocked(event) {
    let username = event.target.getAttribute("username");
    let index = this.state.users.findIndex((user) => user.username == username);

    let newBlocked = 0;
    if (event.target.value == 0) {
      newBlocked = 1;
    }

    let requestUrl = "/api/admin/setblocked";
    let data = {
      username: username,
      newBlocked: newBlocked,
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
        this.setState({
          error: response.data.error,
          errorMessage: response.data.errorMessage,
          success: !response.data.error,
          users: update(this.state.users, {
            [index]: { blocked: { $set: newBlocked } },
          }),
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

  handleChange(event){
    event.preventDefault();
    this.setState({
      [event.target.id]: event.target.value
    })
  }

  componentDidMount() {
    console.log("mount")
    if (!this.props.waitForStart) {
      let requestUrl = "/api/admin/getusers";

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
            users: response.data.users,
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

  handleSubmit(event) {
    let requestUrl3 = 'api/data/setgroupsamount'
    let data = {
    	newNumber: this.state.newNumber
    }
    //console.log("newNumber", data.newNumber)

    axios
      .post(requestUrl3, data, {
        baseURL: this.props.config.proxyPath,
        cancelToken : new axios.CancelToken((c) => {
          this.cancelRequest = c
        })
      })
      .then(response => {
        console.log(requestUrl3, response.data)
        this.setState({
          error: response.data.error,
          errorMessage: response.data.errorMessage,
          groupsAmount: response.data.groupsAmount
        })
      })
      .catch(error => {
        this.setState({
          error: true,
          errorMessage: error.response.data.errorMessage,
          status : errorMessage,
          success: !response.data.error
        })
      })
  }

  render() {
    //console.log()
    let columns = [
      {
        editable: false,
        dataField: "ldap",
        text: "Authentication type",
        formatter: (cell) => {
          return cell ? "Ldap" : "Local";
        },
        sort: true,
      },
      {
        editable: false,
        dataField: "username",
        text: "Username",
        sort: true,
      },
      {
        editable: false,
        dataField: "email",
        text: "Email",
        formatter: (cell) => {
          return <a href={"mailto:" + cell}>{cell}</a>;
        },
        sort: true,
      },
      {
        editable: false,
        dataField: "isAdmin",
        text: "Admin",
        formatter: (cell, row) => {
          return (
            <FormGroup>
              <div>
                <CustomInput
                  type="switch"
                  username={row.username}
                  id={"set-admin-" + row.username}
                  name="isAdmin"
                  onChange={this.handleChangeAdmin}
                  label="Admin"
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
        dataField: "blocked",
        text: "Blocked",
        formatter: (cell, row) => {
          return (
            <FormGroup>
              <div>
                <CustomInput
                  type="switch"
                  username={row.username}
                  id={"set-blocked-" + row.username}
                  name="blocked"
                  onChange={this.handleChangeBlocked}
                  label="Blocked"
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
        dataField: "created",
        text: "Created",
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
        <h2>User management</h2>
        <h3>Coucou</h3>
        <hr />
        <div className=".geno-table-height-div">
          <BootstrapTable
            classes="geno-table"
            wrapperClasses="geno-table-wrapper"
            bootstrap4
            keyField="_id"
            data={this.state.users}
            columns={columns}
            defaultSorted={defaultSorted}
            pagination={paginationFactory()}
            cellEdit={cellEditFactory({
              mode: "click",
              autoSelectText: true,
              beforeSaveCell: (oldValue, newValue, row) => {
                this.updateQuota(oldValue, newValue, row);
              },
            })}
          />
        <Form onSubmit={this.handleSubmit}>
          <Label for="groupsAmount"> Number of groups</Label>
          <Input type="number" name="groupsAmount" id="newNumber" placeholder="" value={this.state.newNumber} onChange={this.handleChange} />
          <Button> Enter </Button>
        </Form>
        </div>
      </div>
    );
  }
}

Users.propTypes = {
  waitForStart: PropTypes.bool,
  config: PropTypes.object,
};
