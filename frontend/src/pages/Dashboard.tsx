import React, { useState } from "react";
import Header from "../components/Header";
import CSVUploadButton from "../components/CSVUploadButton";
import HostnamesTable from "../components/HostnamesTable";
import GlobalStatsCard from "../components/GlobalStatsCard";

export default function Dashboard() {
  return (
    <>
      <Header />
      <CSVUploadButton mb={5} />
      <GlobalStatsCard />
      <HostnamesTable mt={5} />
    </>
  );
}
