import React, { useState } from "react";
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  IconButton,
  useDisclosure,
  TableProps,
} from "@chakra-ui/react";

import { HamburgerIcon } from "@chakra-ui/icons";

import useSWR from "swr";
import { fetcher } from "../services/api";
import RiskBadge from "./RiskBadge";
import IssueListModal from "./IssueListModal";

interface HostnameStats {
  hostname: string;
  total: number;
  riskLevel: number;
  IpAddress: string;
}

export default function HostnamesTable(props: TableProps) {
  const { data, error } = useSWR("/api/report/hostnames/", fetcher);

  console.log(data);

  const { isOpen, onOpen, onClose } = useDisclosure();
  const [hostname, setHostname] = useState("");
  function handleHostnameDetail(hostname: string) {
    setHostname(hostname);
  }

  if (!data) {
    return <>Loading</>;
  }
  return (
    <>
      <IssueListModal
        hostname={hostname}
        onOpen={onOpen}
        onClose={onClose}
        isOpen={isOpen}
      />
      <Table {...props}>
        <Thead>
          <Tr>
            <Th>Hostname</Th>
            <Th>Endereço IP</Th>
            <Th>Vulnerabilidades</Th>
            <Th>Fator de Risco</Th>
            <Th>Detalhes</Th>
          </Tr>
        </Thead>
        <Tbody>
          {data.results.map((hostname: HostnameStats) => {
            return (
              <Tr key={hostname.IpAddress}>
                <Td>{hostname.hostname}</Td>
                <Td>{hostname.IpAddress}</Td>
                <Td>{hostname.total}</Td>
                <Td>
                  <RiskBadge riskLevel={hostname.riskLevel} />
                </Td>
                <Td>
                  <IconButton
                    onClick={(event) => {
                      onOpen();
                      handleHostnameDetail(hostname.hostname);
                    }}
                    aria-label={`Ver Detalhes  do Hostname ${hostname.hostname}`}
                    icon={<HamburgerIcon />}
                  >
                    EXPLORAR
                  </IconButton>
                </Td>
              </Tr>
            );
          })}
        </Tbody>
      </Table>
    </>
  );
}
