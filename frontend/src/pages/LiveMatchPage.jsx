import {
  useEffect,
  useState
} from "react";

import MatchHeader from "../components/MatchHeader";
import StatsTable from "../components/StatsTable";
import Timeline from "../components/Timeline";


const API = "http://localhost:8000";


function LiveMatchPage() {

  const [liveMatches, setLiveMatches] = useState([]);
  const [loading, setLoading] = useState(true);


  // =========================================================
  // FETCH ONE MATCH WITH STATS + EVENTS
  // =========================================================

  const fetchFullMatch = async (matchId) => {

    const [
      matchResponse,
      statsResponse,
      eventsResponse
    ] = await Promise.all([

      fetch(
        `${API}/matches/${matchId}`,
        {
          cache: "no-store"
        }
      ),

      fetch(
        `${API}/matches/${matchId}/team-stats`,
        {
          cache: "no-store"
        }
      ),

      fetch(
        `${API}/matches/${matchId}/events`,
        {
          cache: "no-store"
        }
      ),

    ]);


    const match =
      await matchResponse.json();

    const stats =
      await statsResponse.json();

    const events =
      await eventsResponse.json();


    return {
      match,
      stats,
      events
    };

  };


  // =========================================================
  // FETCH LATEST TWO MATCHES
  // =========================================================

  const fetchLiveMatches = async () => {

    try {

      // -----------------------------------------------------
      // Get all matches
      // -----------------------------------------------------

      const response = await fetch(
        `${API}/matches`,
        {
          cache: "no-store"
        }
      );


      const matches =
        await response.json();


      if (!matches.length) {

        setLiveMatches([]);

        setLoading(false);

        return;
      }


      // -----------------------------------------------------
      // Sort by match number DESC
      //
      // match_006
      // match_005
      // match_004
      // ...
      // -----------------------------------------------------

      const sortedMatches = [
        ...matches
      ].sort(
        (a, b) => {

          const numberA = parseInt(
            a.match_id.replace(
              "match_",
              ""
            )
          );


          const numberB = parseInt(
            b.match_id.replace(
              "match_",
              ""
            )
          );


          return numberB - numberA;

        }
      );


      // -----------------------------------------------------
      // Latest TWO matches
      //
      // Example:
      //
      // match_006
      // match_005
      // -----------------------------------------------------

      const latestTwo =
        sortedMatches.slice(0, 2);


      // -----------------------------------------------------
      // Fetch stats/events for both
      // -----------------------------------------------------

      const completeMatches =
        await Promise.all(

          latestTwo.map(
            (item) =>
              fetchFullMatch(
                item.match_id
              )
          )

        );


      // -----------------------------------------------------
      // Put them back in natural order
      //
      // match_005
      // match_006
      //
      // instead of
      //
      // match_006
      // match_005
      // -----------------------------------------------------

      completeMatches.sort(
        (a, b) => {

          const numberA = parseInt(
            a.match.match_id.replace(
              "match_",
              ""
            )
          );


          const numberB = parseInt(
            b.match.match_id.replace(
              "match_",
              ""
            )
          );


          return numberA - numberB;

        }
      );


      setLiveMatches(
        completeMatches
      );


      setLoading(false);


    } catch (error) {

      console.error(
        "LIVE MATCH ERROR:",
        error
      );

      setLoading(false);

    }

  };


  // =========================================================
  // REAL-TIME REFRESH
  // =========================================================

  useEffect(() => {

    fetchLiveMatches();


    const interval = setInterval(
      fetchLiveMatches,
      2000
    );


    return () =>
      clearInterval(interval);

  }, []);


  // =========================================================
  // LOADING
  // =========================================================

  if (loading) {

    return (

      <div className="page-message">

        Loading live matches...

      </div>

    );

  }


  // =========================================================
  // NO MATCHES
  // =========================================================

  if (!liveMatches.length) {

    return (

      <div className="page-message">

        No live matches available.

      </div>

    );

  }


  // =========================================================
  // UI
  // =========================================================

  return (

    <main className="page-container">


      {/* =====================================================
          PAGE HEADER
      ===================================================== */}

      <div className="page-heading">

        <div
            className="page-heading-text"
            style={{ textAlign: "left" }}
        >

          <span className="section-label">
            LIVE ANALYTICS
          </span>

          <h1>
            Live Matches
          </h1>

          <p>
            Real-time football analytics powered by
            Kafka and Spark Streaming.
          </p>

        </div>


        <div className="refresh-status">

          ● Updating every 2 seconds

        </div>

      </div>


      {/* =====================================================
          BOTH LIVE MATCHES
      ===================================================== */}

      <div className="live-matches-list">


        {liveMatches.map(
          ({
            match,
            stats,
            events
          }) => (

            <div
              className="live-match-block"
              key={match.match_id}
            >


              {/* MATCH SCORE */}

              <MatchHeader
                match={match}
                events={events}
                live={true}
              />


              {/* ANALYTICS */}

              <div className="analytics-grid">


                <StatsTable
                  match={match}
                  stats={stats}
                />


                <Timeline
                  events={events}
                  limit={10}
                />


              </div>


            </div>

          )
        )}


      </div>


    </main>

  );

}


export default LiveMatchPage;