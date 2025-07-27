/**********************************************************************************************************
 * @file        NavBar.jsx
 * @description Navigation bar component using React-Bootstrap, displaying links based on user login state.
 *              Includes links for About, Project, Resource, Sign In, Sign Up, and Sign Out.
 *              Handles user logout by updating login state.
 * @team        SheCodes-Hub (MSITM'26 @ McComb School of Business, UT Austin)
 * @created     2025-07-26
 * @version     v1.0.0
 **********************************************************************************************************/
import React from "react";
import { Navbar, Nav, Container } from "react-bootstrap";
import { NavLink } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";

const NavBar = ({ isLoggedIn, setIsLoggedIn }) => {

  const handleLogout = () => {
    // setting 'isLoggedIn' to false if user click the logout
    setIsLoggedIn(false);
  };

  return (
    <Navbar
      expand="lg"
      className="shadow-sm"
      style={{ backgroundColor: "#4B0082", minHeight: "12vh" }}
      variant="dark"
    >
      <Container>
        <LinkContainer to="/">
          <Navbar.Brand>Hardware Resource Management Portal</Navbar.Brand>
        </LinkContainer>
        <Navbar.Toggle aria-controls="main-navbar-nav" /> {/*getting collapsable three horizontal line 'mobile compatible'*/}
        <Navbar.Collapse id="main-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link as={NavLink} to="/about" end>
              About
            </Nav.Link>
            {isLoggedIn ? (
              <React.Fragment>
                <Nav.Link as={NavLink} to="/project" end>
                  Project
                </Nav.Link>
                <Nav.Link as={NavLink} to="/resource" end>
                  Resource
                </Nav.Link>
                <Nav.Link as={NavLink} to="/about" onClick={handleLogout} end>
                  Sign Out
                </Nav.Link>
              </React.Fragment>
            ) : (
              <React.Fragment>
                <Nav.Link as={NavLink} to="/login" end>
                  Sign In
                </Nav.Link>
                <Nav.Link as={NavLink} to="/signup" end>
                  Sign Up
                </Nav.Link>
              </React.Fragment>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavBar;
