import React from "react";

function Search({ onSearch }) {
  return (
    <div className="search">
      <label className="btn" htmlFor="search">
        Search ToDo Lists:{" "}
      </label>

      <input
        className="box-border"
        type="text"
        id="search"
        placeholder="Type a name to search..."
        onChange={onSearch}
      />
    </div>
  );
}

export default Search;
