import React, { Component } from "react";
import axios from "axios";
import { Button, CardBody, Row, Container, Col, Card, CardTitle, CardSubtitle, CardHeader, ListGroup, ListGroupItem} from "reactstrap";
import BootstrapTable from "react-bootstrap-table-next";
import PropTypes from "prop-types";
import Identicon from "react-identicons";
import { Redirect } from "react-router";
import ProgressBar from 'react-bootstrap/ProgressBar'


export default class Dashboard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      start: false,
      top_users: [],
      top_groups: [],
      groups_names: []
    };
    this.setStart = this.setStart.bind(this);
  }

  setStart() {
    this.setState({ start: true });
  }

  componentDidMount(){
    console.log("mount")
    if (!this.props.waitForStart) {
      let requestUrl_users = 'api/data/getusersamount';
      let requestUrl_answers = 'api/data/getanswersamount';
      let requestUrl_groups = 'api/data/getgroupsamount';
      let requestUrl_top = 'api/data/gettopannotation';
      let requestUrl_groupsnames = 'api/data/getgroupsnames';
      let requestUrl_genes = '/api/data/countallgenes';

      Promise.all([
        axios.get(requestUrl_users, {
          baseURL: this.props.config.proxyPath,
          cancelToken: new axios.CancelToken((c) => {
            this.cancelRequest = c;
            }),
        }),
        axios.get(requestUrl_answers, {
          baseURL: this.props.config.proxyPath,
          cancelToken: new axios.CancelToken((c) => {
            this.cancelRequest = c;
          }),
        }),
        axios.get(requestUrl_groups, {
          baseURL: this.props.config.proxyPath,
          cancelToken: new axios.CancelToken((c) => {
            this.cancelRequest = c;
          }),
        })
      ])
      .then(([response_users, response_answers, response_groups ]) => {
        console.log(requestUrl_users, response_users.data);
        console.log(requestUrl_answers,response_answers.data);
        console.log(requestUrl_groups,response_groups.data);
        this.setState({
          isLoading: false,
          error: [response_users.data.error,response_answers.data.error, response_groups.data.error],
          errorMessage: [response_users.data.errorMessage, response_answers.data.errorMessage, response_groups.data.errorMessage],
          usersAmount: response_users.data.usersAmount,
          answersAmount: response_answers.data.answersAmount,
          groupsAmount: response_groups.data.groupsAmount
        });
      })

      axios
        .get(requestUrl_top, {
        baseURL: this.props.config.proxyPath,
        cancelToken: new axios.CancelToken((c) => {
          this.cancelRequest = c;
          }),
        })
        .then((response_top) => {
          console.log(requestUrl_top, response_top.data);
          this.setState({
            error: response_top.data.error,
            errorMessage: response_top.data.errorMessage,
            top_groups: response_top.data.top_groups,
            top_users: response_top.data.top_users
          });

        })

      axios
        .get(requestUrl_groupsnames, {
          baseURL: this.props.config.proxyPath,
          cancelToken: new axios.CancelToken((c) => {
            this.cancelRequest = c;
          }),
        })
        .then((response_groupsnames) => {
          this.setState({
            'error': response_groupsnames.data.error,
            'errorMessage': response_groupsnames.data.errorMessage,
            'groups_names': response_groupsnames.data.groups_names
          });
        })

      axios
        .get(requestUrl_genes, {
          baseURL: this.props.config.proxyPath,
          cancelToken: new axios.CancelToken((c) => {
            this.cancelRequest = c
          }),
        })
        .then((response_genes) => {
          this.setState({
            'error': response_genes.data.error,
            'errorMessage': response_genes.data.errorMessage,
            'genes': response_genes.data.genes
          })
        })
    }
  }


  render() {
    let html = <Redirect to="/annotator" />;
    let columns_users = [
      {
        editable: false,
        dataField:"username",
        text: "User"
      },
      {
        editable: false,
        dataField: "score",
        text: "Score"
      }
    ]

    let columns_groups = [
      {
        editable: false,
        dataField: "name",
        text: "Group",
      },
      {
        editable: false,
        dataField: "score",
        text: "Score",
      }
    ]

    if (this.state.start === false) {
      html = (
        <Container>
          <Row>
            <Col>
              <Card className="dashboard-usercards">
                <br></br>
                <CardTitle tag="h3">
                  {this.props.config.user.username}
                </CardTitle>
                <CardSubtitle></CardSubtitle>
                <CardBody>
                  <br></br>
                  <Container>{this.state.groups_names[this.props.config.user.group-1]}</Container>
                  <br></br>
                  <Identicon
                    size={100}
                    string={this.props.config.user.username}
                  />
                </CardBody>
              </Card>
            </Col>
            <Col>
              <Card body outline className="dashboard-progresscards">
                <CardTitle>Project progress</CardTitle>
                <CardBody>
                  <ProgressBar>
                    <ProgressBar striped variant="success" now={this.answersAmount} key={1} max={this.state.genes} label={this.answersAmount}/>
                  </ProgressBar>
                </CardBody>
                <hr></hr>
                <Button success>Get Started</Button>
              </Card>
            </Col>
            <Col>
              <Row>
                <Card className="dashboard-statcards">
                  <CardHeader>Annotated genes</CardHeader>
                  <CardBody>{this.state.answersAmount}</CardBody>
                </Card>
              </Row>
              <Row>
                <Card className="dashboard-statcards">
                  <CardHeader>Number of annotators</CardHeader>
                  <CardBody>{this.state.usersAmount}</CardBody>
                </Card>
              </Row>
              <Row>
                <Card className="dashboard-statcards">
                  <CardHeader>Number of groups</CardHeader>
                  <CardBody>{this.state.groupsAmount} </CardBody>
                </Card>
              </Row>
            </Col>
          </Row>
          <Row>
            <Col>
              <Card className="dashboard-hystorycards">
                <ListGroup>
                  <ListGroupItem color="warning ">
                    gene <Button color="success">Resume</Button>
                  </ListGroupItem>
                  <ListGroupItem color="danger">
                    gene <Button color="success">Resume</Button>
                  </ListGroupItem>
                  <ListGroupItem color="success">
                    gene <Button color="success">Resume</Button>
                  </ListGroupItem>
                </ListGroup>
              </Card>
            </Col>
            <Col>
              <Card>
                <Col>
                  <Card>
                    <CardHeader className="center-div">
                      Top 3 annotators
                    </CardHeader>
                    <CardBody>
                      <BootstrapTable
                        keyField = "_id"
                        data={this.state.top_users}
                        columns= {columns_users}
                      />
                    </CardBody>
                  </Card>
                </Col>
                <Col>
                  <Card>
                    <CardHeader className="center-div">Top 3 groups</CardHeader>
                    <CardBody>
                      <BootstrapTable
                        keyField = "_id"
                        data={this.state.top_groups}
                        columns= {columns_groups}
                      />
                    </CardBody>
                  </Card>
                </Col>
              </Card>
            </Col>
          </Row>
        </Container>
      );
    }
    return html;

  }
}
Dashboard.propTypes = {
  waitForStart : PropTypes.bool,
  config: PropTypes.object,
};
