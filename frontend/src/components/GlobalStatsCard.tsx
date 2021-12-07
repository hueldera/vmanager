import React, { useState } from "react";
import { StatGroup, Stat, StatLabel, StatNumber } from "@chakra-ui/react";

import useSWR from "swr";
import { fetcher } from "../services/api";

export default function GlobalStatsCard() {
  const { data, error } = useSWR("/api/report/", fetcher);

  if (!data) {
    return <>Loading</>;
  }
  const { totalIssuesCount, fixedIssuesCount, hostnamesRiskAvg } = data.stats;
  return (
    <>
      <StatGroup border="1px" borderRadius="md" borderColor="gray.200" p={10}>
        <Stat>
          <StatLabel>Vulnerabilidades Encontradas</StatLabel>
          <StatNumber>{totalIssuesCount}</StatNumber>
        </Stat>
        <Stat>
          <StatLabel>Vulnerabilidades Ativas</StatLabel>
          <StatNumber>{totalIssuesCount - fixedIssuesCount}</StatNumber>
        </Stat>
        <Stat>
          <StatLabel>Vulnerabilidades Corrigidas</StatLabel>
          <StatNumber>{fixedIssuesCount}</StatNumber>
        </Stat>
        <Stat>
          <StatLabel>Média de CVSS Score</StatLabel>
          <StatNumber>{hostnamesRiskAvg}</StatNumber>
        </Stat>
      </StatGroup>
    </>
  );
}
