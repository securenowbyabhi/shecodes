/**********************************************************************************************************
 * @file        ResourceComponent.jsx
 * @description TO-BE-DEVELOPED
 * @team        SheCodes-Hub (MSITM'26 @ McComb School of Business, UT Austin)
 * @created     2025-07-26
 * @version     v1.0.0
 **********************************************************************************************************/
import React from 'react';
import ReusableHeaderComponent from './ReusableHeaderComponent'

const ResourceComponent = () => {
    return (
      <div >
        <ReusableHeaderComponent 
          title="Welcome to Resource Management" 
          message="You can explore your assigned projects, view associated hardware, and manage Check-In/Check-Out of resources." 
        />
      </div>
    );
  };

export default ResourceComponent;