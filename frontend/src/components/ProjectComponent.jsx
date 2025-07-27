/**********************************************************************************************************
 * @file        ProjectComponent.jsx
 * @description TO-BE-DEVELOPED
 * @team        SheCodes-Hub (MSITM'26 @ McComb School of Business, UT Austin)
 * @created     2025-07-26
 * @version     v1.0.0
 **********************************************************************************************************/
import React from 'react';
import ReusableHeaderComponent from './ReusableHeaderComponent'

const ProjectComponent = () => {
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