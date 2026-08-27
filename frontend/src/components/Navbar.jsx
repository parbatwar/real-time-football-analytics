import { NavLink } from "react-router-dom";


function Navbar() {
  return (
    <header className="navbar">

      <div className="brand">

        <h1 style={{ textAlign: "left" }}>
          Football Analytics
        </h1>

      </div>


      <nav>

        <NavLink
          to="/"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Live
        </NavLink>

        <NavLink
          to="/history"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Match History
        </NavLink>

      </nav>

    </header>
  );
}


export default Navbar;