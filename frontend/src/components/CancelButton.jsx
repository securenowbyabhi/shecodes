/******************************************************************************************
 * @file        CancelButton.jsx
 * @description Reusable Cancel button that resets form and navigates to 'About' page.
 * @team        SheCodes-Hub (MSITM'26 @ McComb School of Business, UT Austin)
 * @created     2025-07-27
 * @version     v1.0.0
**********************************************************************************************************/
import React from 'react';
import { useNavigate } from 'react-router-dom';

function CancelButton(props) {

  const navigate = useNavigate();

  // Access props 
  const resetForm = props.resetForm;
  // Redirect to provided path else, default to about page if not passed
  const redirectTo = props.redirectTo || '/about'; 

  const handleCancel = () => {
    if (resetForm) {
        resetForm();
    }
    navigate(redirectTo);
  };

  return (
    <button type="button" onClick={handleCancel} style={{ marginLeft: '0.5rem' }}>
      Cancel
    </button>
  );
}

export default CancelButton;
