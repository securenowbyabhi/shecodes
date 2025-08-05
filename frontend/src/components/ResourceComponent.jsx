/**********************************************************************************************************
 * @file        ResourceComponent.jsx
 * @description Component to show the project details assigned to logged in user as well as
 *              handle the Resource Check-in/Check-out functionality
 * @team        SheCodes-Hub (MSITM'26 @ McComb School of Business, UT Austin)
 * @created     2025-07-26
 * @version     
 * v1.0.0       Initial Draft(Structure)           2025-07-26
 * v1.0.1       Developed the feature              2025-08-02
 **********************************************************************************************************/
import React, { useEffect,useState } from "react";
import ReusableHeaderComponent from "./ReusableHeaderComponent";
import { useOutletContext  } from 'react-router-dom';
import { postToEndpoint, getFromEndpoint } from "../utils/apiHelpers";
import { showSuccess, showError } from "../utils/toastUtils";
import "../utils/spinner.css";

const ResourceComponent = () => {

  const { setIsLoggedIn } = useOutletContext();

  //setting context variable 'isLoggedIn' to true to have same tabs look and feel when user is loggedIn as compare to logged out of app
  useEffect(() => {
    setIsLoggedIn(true);
  }, [setIsLoggedIn]);

  const [spinnerLoading, setSpinnerLoading] = useState(false);

  //checkOut attribute in projectForm will hold checkedOut quantities per hardware [0,0]
  const [projectForm, setProjectForm] = useState({projectid: "",checkedOut: [],});

  //Sample useState attributes for hardwareForm:  { hardwareid: "", capacity: 0, available: 0, userinput: 0 }
  const [hardwareForm, setHardwareForm] = useState([]);

  const [projectDataLoaded, setProjectDataLoaded] = useState(false);

  /*********************************************************************************************
  * Method: 'getProjectDetails'
  * Purpose: To request the project and inventory details from backend and
  *           prepare the 'projectForm' and 'hardwareForm' datastructure to display data on UI.
  **********************************************************************************************/
  const getProjectDetails = async (event) => {

    console.log("project id: ", event.target.value);
    event.preventDefault();

    try {

      setSpinnerLoading(true); // loading spinner

      //Setting to false initially since, if someone enter new projectId in 
      // already loaded form it should refresh the second form with latest data.
      setProjectDataLoaded(false);

      const { ok, data } = await getFromEndpoint("projectstatus", {
        projectid: projectForm.projectid,
      });
      console.log("Project Data from backend :", data);

      //This will hold the actual response from the server having message and data(JSON format)
      const response = data.response;

      if (ok) {

        //populating projectForm with project Id and hardware qty already checked out
        setProjectForm((prev) => ({
          ...prev,
          checkedOut: response.checkedOut || [],
        }));

        //populating hardwareForm with inventory details received from backend
        const inventory = response.inventory.map((hwObj) => ({
          hardwareid: hwObj.hardwareid,
          capacity: hwObj.capacity,
          available: hwObj.available,
          userinput: 0,
        }));
        setHardwareForm(inventory);

        setProjectDataLoaded(true); //setting flag to load the section having project along with inventory details on UI
        showSuccess(`Success: ${data.message}`);

      } else {
        showError(`Error: ${data.message}`);
      }

    } catch (error) {
      showError(`Error: ${error.message}`);
    } finally {
      setSpinnerLoading(false); // spinner loading ended
    }
  };

  /*********************************************************************************************
  * Method: 'handleUserInputChange'
  * Purpose: Method to keep track of the hardware Request by the user specific to harware type
  **********************************************************************************************/
  const handleUserInputChange = (index, value) => {

    setHardwareForm((prev) => {
      const inventoryData = [...prev];
      inventoryData[index] = { ...inventoryData[index], userinput: value }; 
      return inventoryData;
    });

  };

  /********************************************************************************************************
  * Method: 'handleCheckInCheckOut'
  * Purpose: Method to handle the hardware check-out/check-in feature by the user for the requested number
  ********************************************************************************************************/
  const handleCheckInCheckOut = async (action) => {

    setSpinnerLoading(true);

    let anyQtyToCheckInCheckOut = 0
    
    //Handle all the edge case scenario - validating the requested number before proceeding
    for (let i = 0; i < hardwareForm.length; i++) {

      const inputQty = hardwareForm[i].userinput;
	    const available = hardwareForm[i].available;
	    const checkedOut = projectForm.checkedOut[i];

      if(inputQty < 0) {
        showError(`Error: Negative quantity ${inputQty} for ${hardwareForm[i].hardwareid}.`);
        setSpinnerLoading(false);
        return;
      } 
	  
	    if(action === 'checkout' && inputQty > available) {
        showError(`Error: Cannot check out ${inputQty} quantity, only ${available} available for ${hardwareForm[i].hardwareid}.`);
        setSpinnerLoading(false);
        return;
      } 
	  
	    if(action === 'checkin' && inputQty > checkedOut) {
	      showError(`Error: Cannot check in ${inputQty} quantity, when checked out is ${checkedOut} for ${hardwareForm[i].hardwareid}.`);
		    setSpinnerLoading(false);
        return;
	    }
          
      if(inputQty > 0 && anyQtyToCheckInCheckOut === 0) {
        anyQtyToCheckInCheckOut = inputQty
      } 

    }

    //Throwing error if user is simply clicking check-out/check-in without requesting any number
    if(anyQtyToCheckInCheckOut === 0) {
        showError(`Error: There is nothing to ${action}.`);
        setSpinnerLoading(false);
        return;
    } 

    try {

      //inventory payload to send to backend API to process the check-out/check-in request
      const inventoryPayload = hardwareForm.map((hwObj) => ({
        hardwareid: hwObj.hardwareid,
        quantity: hwObj.userinput,
      }));

      //POST call to backend api - 'checkincheckout'
      const { ok, data } = await postToEndpoint("checkincheckout", {
        projectid: projectForm.projectid,
        inventory: inventoryPayload,
        action: action,
      });

      if (ok) {

        showSuccess(`Success: ${data.message}`);

        //Updating 'projectForm' datastructure to refelect the updated count on UI
        setProjectForm((prev) => {
          const updatedCheckedOut = prev.checkedOut.map((qty, i) => {
			    const userInputQty = hardwareForm[i].userinput;
            return action === "checkout"? qty + userInputQty : qty - userInputQty;
          });
          return {...prev,checkedOut: updatedCheckedOut};
        });

        //Updating 'hardwareForm' datastructure to reflect the updated count of inventory on UI
        const updatedForm = hardwareForm.map((hwObj) => ({
          ...hwObj,
          available: action === "checkout" ? hwObj.available - hwObj.userinput : hwObj.available + hwObj.userinput,
          userinput: 0,
        }));
        setHardwareForm(updatedForm);

      } else {
        showError(`Error: ${data.message || "Unknown error"}.`);
      }
    } catch (error) {
      showError(`Error: ${error.message}.`);
    } finally {
      setSpinnerLoading(false); //disabling spinner load
    }
  };

  /**************************************************
  * UI-Design starts here
  ***************************************************/
  return (

    <div>

      <div>
        <ReusableHeaderComponent
          title="Welcome to Resource Management"
          message="You can explore your assigned projects, view associated hardware, and manage Check-In/Check-Out of resources."
        />
      </div>

      <div style={{ width: "80vw", maxWidth: "700px", margin: "2.5rem auto" }}>

        {/*Spinner to load while requesting backend APIs */}
        {spinnerLoading && (
          <div className="spinner-overlay">
            <div className="spinner" />
            <p>Loading data...</p>
          </div>
        )}

        {/* Project Form */}
        <form onSubmit={getProjectDetails} style={{ marginBottom: "2rem", marginTop: "2rem" }}>
          <div style={{ display: "flex", alignItems: "center" }}>
            <label style={{ width: "5rem" }}>Project ID:</label>
            <input type="text" name="projectid" value={projectForm.projectid}
              onChange={(event) =>
                setProjectForm((prev) => ({ //directly using useState function here on onChange, which is an intresting way of setting the usestate attributes
                  ...prev,
                  projectid: event.target.value,
                }))
              }
              required
            />
            <button style={{ marginLeft: "2rem" }} type="submit">
              Check Project
            </button>
          </div>
        </form>

        {/* Loading second part of the UI, once project Id is validated and details are successfully retrieved */}
        {projectDataLoaded && (
          <React.Fragment>
            <div style={{ marginBottom: "2rem" }}>
              <table style={{width: "25vw", maxWidth: "100%", fontSize: "15px", textAlign: "center"}}>
                <thead>
                  <tr>
                    <th></th>
                    <th>Checked Out Quantity</th>
                  </tr>
                </thead>
                <tbody>
                  {/*Loop through projectForm datastructure to print the checkout quantity */}
                  {projectForm.checkedOut.map((qty, index) => (
                    <tr key={index}>
                      <td>Hardware SET {index + 1}:</td>
                      <td>{qty}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div style={{ marginTop: "2rem" }}>

              {/* Hardware Form to show the Inventory details and userInput for user to request/return hardwares */}
              <form>
                <h6>Manage Hardware Check-In/Check-Out feature</h6>

                <table style={{width: "100%",fontSize: "15px",textAlign: "center",border: "1px solid black"}}>
                  <thead>
                    <tr>
                      <th></th>
                      <th>Capacity</th>
                      <th>Availability</th>
                      <th>Request</th>
                    </tr>
                  </thead>
                  <tbody>
                  {/*Loop through hardwareForm datastructure to print the hardware details */}
                    {hardwareForm.map((hwObj, index) => (
                      <tr key={hwObj.hardwareid}>
                        <td>Hardware SET {index + 1}:</td>
                        <td>{hwObj.capacity}</td>
                        <td>{hwObj.available}</td>
                        <td>
                          <input 
                            type="number" 
                            value={hwObj.userinput === 0 ? "":hwObj.userinput}
                            onChange={(event) =>
                              handleUserInputChange(index, Number(event.target.value))
                            }
                            placeholder="Enter quantity"
                          />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                {/* Check-In and Check-Out Buttons section */}
                <div style={{display: "flex", gap: "1rem", marginTop: "1.5rem",justifyContent: "flex-end"}}>
                  <button type="button" onClick={()=>handleCheckInCheckOut("checkout")}>Check Out</button>
                  <button type="button" onClick={()=>handleCheckInCheckOut("checkin")}>Check In</button>
                </div>
              </form>
            </div>
          </React.Fragment>
        )}
      </div>
    </div>
  );
};

export default ResourceComponent;
