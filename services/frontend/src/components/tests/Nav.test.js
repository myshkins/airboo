import React from "react";
import { BrowserRouter } from 'react-router-dom'
import { render, screen } from '@testing-library/react'
import "@testing-library/jest-dom"
import userEvent from "@testing-library/user-event"
import Nav from "../Nav"


describe("navbar", () => {
  it("renders the navbar", () => {
    const { container } = render(<Nav />, {wrapper: BrowserRouter})
    expect(container).toMatchSnapshot()
  })
})