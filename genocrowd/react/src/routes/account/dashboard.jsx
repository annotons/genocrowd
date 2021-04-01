import React, { Component } from "react";
import axios from "axios";
import {
  Button,
  CardBody,
  Row,
  Container,
  Col,
  Card,
  CardTitle,
  CardSubtitle,
  CardImg,
  CardHeader,
  Progress,
  ListGroup,
  ListGroupItem,
  Table,
} from "reactstrap";
import PropTypes from "prop-types";
import Identicon from "react-identicons";
import { Redirect } from "react-router";

export default class Dashboard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      start: false,
    };
    this.setStart = this.setStart.bind(this);
  }

  setStart() {
    this.setState({ start: true });
  }

  componentDidMount(){
    if (!this.props.waitForStart) {
      let requestUrl_users = 'api/data/getusersamount';
      let requestUrl_answers = 'api/data/getanswersamount';
      
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
        })
      ])
      .then(([response_users, response_answers]) => {
        console.log([requestUrl_users, requestUrl_answers], [response_users.data, response_answers]);
        this.setState({
          isLoading: false,
          error: [response_users.data.error,response_answers.data.error],
          errorMessage: [response_users.data.errorMessage, response_answers.data.errorMessage],
          usersAmount: response_users.data.usersAmount,
          answersAmount: response_answers.data.answersAmount
        });
      })
    }
  }


  render() {
    let html = <Redirect to="/annotator" />;
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
                <CardSubtitle>GroupName</CardSubtitle>
                <CardBody>
                  <br></br>
                  <Container></Container>
                  <Progress value={2 * 5}></Progress>
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
                <CardImg
                  size="100%"
                  src="../../../../static/logo/fauxcamembert.png"
                ></CardImg>
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
                  <CardBody>15</CardBody>
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
                      Top annotators
                    </CardHeader>
                    <CardBody>
                      <Table className="center-div">
                        <thead>
                          <tr>
                            <th>Weekly</th>
                            <th>Global</th>
                          </tr>
                        </thead>
                      </Table>
                    </CardBody>
                  </Card>
                </Col>
                <Col>
                  <Card>
                    <CardHeader className="center-div">Top groups</CardHeader>
                    <CardBody>
                      <Table className="center-div">
                        <thead>
                          <tr>
                            <th>Weekly</th>
                            <th>Global</th>
                          </tr>
                        </thead>
                      </Table>
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
