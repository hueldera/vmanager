import React from "react";
import axios from "axios";
import { Button, ButtonProps } from "@chakra-ui/react";
import { TriangleUpIcon } from "@chakra-ui/icons";

export default function CSVUploadButton(props: ButtonProps) {
  const csvInputRef = React.useRef<HTMLInputElement>(null);

  function handleCsvFileFinder() {
    if (csvInputRef.current) {
      csvInputRef.current.click();
    }
  }

  async function handleCsvUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const formData = new FormData();
    formData.append("file", event.target.files[0]);
    const response = await axios.post("/api/upload_csv/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  }

  return (
    <>
      <input
        hidden
        onChange={handleCsvUpload}
        type="file"
        ref={csvInputRef}
        accept=".csv"
      />
      <Button {...props} onClick={handleCsvFileFinder} colorScheme="blue">
        <TriangleUpIcon mr={5} /> Carregar CSV
      </Button>
    </>
  );
}
