/**********************************************************************************************************
 * @file        ProjectComponent.jsx
 * @description TO-BE-DEVELOPED
 * @team        SheCodes-Hub (MSITM'26 @ McComb School of Business, UT Austin)
 * @created     2025-07-26
 * @version     
 * v1.0.0       Initial Draft(Structure)           2025-07-26
 **********************************************************************************************************/
import React,{useEffect} from 'react';
import ReusableHeaderComponent from './ReusableHeaderComponent'
import { useOutletContext  } from 'react-router-dom';

const ProjectComponent = () => {

    const { setIsLoggedIn } = useOutletContext();

    //setting context variable 'isLoggedIn' to true to have same tabs look and feel when user is loggedIn as compare to logged out of app
    useEffect(() => {
      setIsLoggedIn(true);
    }, [setIsLoggedIn]);

    return (
      <div >
        <ReusableHeaderComponent 
          title="Welcome to Project page" 
          message="You can create new project here." 
        />
      </div>
    );
  };

export default ProjectComponent;