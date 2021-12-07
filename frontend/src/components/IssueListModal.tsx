import React from "react";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  Table,
  Tr,
  Td,
  Thead,
  Tbody,
  Th,
  Checkbox,
  Text,
  useToast,
} from "@chakra-ui/react";
import useSWR, { useSWRConfig } from "swr";
import { fetcher } from "../services/api";
import axios from "axios";
import RiskBadge from "./RiskBadge";
// @ts-ignore
import cookie from "react-cookies";

interface IssueListModalProps {
  hostname: string;
  isOpen: boolean;
  onOpen: () => void;
  onClose: () => void;
}

interface Issue {
  id: number;
  vulnerability: {
    id: number;
    title: string;
    cvssScore: number;
  };
  createdAt: string;
  fixDate: string;
}

export default function IssueListModal({
  hostname,
  onOpen,
  onClose,
  isOpen,
}: IssueListModalProps) {
  const toast = useToast();
  const { mutate } = useSWRConfig();

  async function handleToggleIssueResolution(id: number) {
    try {
      const response = await axios.post(`/api/issues/toggle/${id}/`, {
        headers: {
          "x-csrftoken": cookie.load("csrftoken"),
        },
      });
      if (response.status !== 200) {
        throw Error();
      }
      toast({
        title: "Você é incrível!",
        description: "O status da vulnerabilidade foi alterado.",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
      mutate(`/api/issues/?hostname=${hostname}`);
      mutate(`/api/report/`);
    } catch {
      toast({
        title: "Ocorreu um problema... :(",
        description: "Sua alteração não pode ser realizada no momento.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  }

  const { data, error } = useSWR(`/api/issues/?hostname=${hostname}`, fetcher);

  if (!data) {
    return <>Loading...</>;
  }
  return (
    <>
      <Modal
        onClose={onClose}
        isOpen={isOpen}
        scrollBehavior="outside"
        size="full"
      >
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>{hostname.toUpperCase()}</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Table>
              <Thead>
                <Tr>
                  <Th>Corrigida?</Th>
                  <Th>Vulnerabilidade</Th>
                  <Th>Score CVSS</Th>
                  <Th>Adicionada Em</Th>
                </Tr>
              </Thead>
              <Tbody>
                {data.results.map((issue: Issue) => {
                  return (
                    <Tr key={issue.vulnerability.id}>
                      <Td>
                        <Checkbox
                          size="lg"
                          colorScheme="green"
                          isChecked={issue.fixDate !== null}
                          onChange={(event) =>
                            handleToggleIssueResolution(issue.id)
                          }
                        ></Checkbox>
                      </Td>
                      <Td>
                        <Text
                          decoration={issue.fixDate !== null && "line-through"}
                          fontSize="md"
                        >
                          {issue.vulnerability.title}
                        </Text>
                      </Td>
                      <Td>
                        <RiskBadge riskLevel={issue.vulnerability.cvssScore} />
                      </Td>
                      <Td>{new Date(issue.createdAt).toLocaleString()}</Td>
                    </Tr>
                  );
                })}
              </Tbody>
            </Table>
          </ModalBody>
          <ModalFooter>
            <Button onClick={onClose}>Fechar</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}
