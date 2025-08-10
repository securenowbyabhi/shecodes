/**********************************************************************************************************
 * @file        UserCredentialForm.jsx
 * @description Reusable form component for user credentials (User ID and Password).
 * @team        SheCodes-Hub (MSITM'26 @ McComb School of Business, UT Austin)
 * @created     2025-08-07
 * @version     v1.0.0
 **********************************************************************************************************/

import React from 'react';

function UserCredentialForm({ formData, handleChange }) {
  return (
    <>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
        <label style={{ width: '100px' }}>User ID</label>
        <input
          type="text"
          name="userid"
          value={formData.userid}
          onChange={handleChange}
          required
        />
      </div>

      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
        <label style={{ width: '100px' }}>Password</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
      </div>
    </>
  );
}

export default UserCredentialForm;
