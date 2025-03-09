import React, { useState } from "react";
import { Box, Button, Typography, Paper, CircularProgress,Modal } from "@mui/material";
import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile";
import { openDialog } from "uploadcare-widget";
import axios from "axios";

const ResumeUpload = () => {
  const [fileUrl, setFileUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [openSuccessModal, setOpenSuccessModal] = useState(false);

  const handleUpload = () => {
    openDialog({}, { publicKey: "8eeb05a138df98a3c92f" }).done((file) => {
      setLoading(true);
      file.done(async (file) => {
        setFileUrl(file.cdnUrl);
      });
      setLoading(false);
    });
  };

  const handleSubmit = async () => {
    if (!fileUrl) {
      alert("Please upload a resume first.");
      return;
    }

    try {
      const response = await fetch(fileUrl);
      const blob = await response.blob();
      const file = new File([blob], "resume.pdf", { type: "application/pdf" });
      const formData = new FormData();
      formData.append("resume", file);
      formData.append("cvurl", fileUrl);
      console.log(fileUrl);

      const uploadResponse = await axios.post(
        "https://highimpacttalent.onrender.com/api-v1/ai/resume-pool",
        formData,
      );
        console.log("Resume upload response:", uploadResponse.data);
    } catch (error) {
      console.error("Resume submission error:", error);
      alert("Failed to submit resume. Please try again.");
    } 
    setTimeout(() => {
        setOpenSuccessModal(true);
        }, 2000);
  };

  return (
    <Box sx={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", px: 3 }}>
      <Paper elevation={3} sx={{ p: 4, textAlign: "center", width: 400 }}>
        <Typography variant="h5" fontWeight="bold" gutterBottom>
          Upload Your Resume
        </Typography>
        <Typography variant="body2" color="textSecondary" mb={2}>
          Upload your resume to explore job opportunities.
        </Typography>
        <Box
          onClick={handleUpload}
          sx={{
            border: "2px dashed #1976d2",
            p: 3,
            cursor: "pointer",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            borderRadius: 2,
          }}
        >
          {loading ? (
            <CircularProgress />
          ) : fileUrl ? (
            <>
              <InsertDriveFileIcon color="primary" fontSize="large" />
              <Typography variant="body2">Resume Uploaded</Typography>
            </>
          ) : (
            <>
              <InsertDriveFileIcon color="action" fontSize="large" />
              <Typography variant="body2">Click here to upload resume</Typography>
            </>
          )}
        </Box>
        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          sx={{ mt: 3 }}
          disabled={!fileUrl}
        >
          Submit Resume
        </Button>
      </Paper>
       {/* Success Modal */}
       <Modal open={openSuccessModal} onClose={() => setOpenSuccessModal(false)}>
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            bgcolor: "white",
            boxShadow: 24,
            p: 4,
            borderRadius: 3,
            textAlign: "center",
          }}
        >
          <Typography variant="h6" color="primary">Resume Sent Successfully!</Typography>
          <Typography variant="body2" mt={2}>Your resume has been added to the pool.</Typography>
          <Button onClick={() => setOpenSuccessModal(false)} variant="contained" color="primary" sx={{ mt: 3 }}>
            Close
          </Button>
        </Box>
      </Modal>
    </Box>
  );
};

export default ResumeUpload;
