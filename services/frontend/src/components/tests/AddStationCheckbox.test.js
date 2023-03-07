import React from "react";
import { BrowserRouter } from 'react-router-dom'
import { getByLabelText, render, screen } from '@testing-library/react'
import "@testing-library/jest-dom"
import userEvent from "@testing-library/user-event"
import AddStationCheckbox from "../AddStationCheckbox";

const onChangeMock = jest.fn()

describe("AddStationCheckbox", () => {
  it("renders a checkbox input with the given name", () => {
    const { container } = render(
      <AddStationCheckbox
        key={"01234"}
        name={"01234"}
        pollutants={["pm25_aqi", "pm10_aqi"]}
        value={"Santa's Workshop"}
        checked={true}
        onChange={onChangeMock}
      />
    )
    expect(container).toMatchSnapshot()
    expect(screen.getByRole("checkbox")).toBeChecked()
  })
})
