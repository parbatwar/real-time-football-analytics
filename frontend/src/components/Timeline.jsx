function Timeline({
  events = [],
  limit = 10
}) {

  const visibleEvents = events.slice(0, limit);

  return (
    <section className="analytics-section timeline-section">

      <div className="section-heading">

        <span className="section-label">
          LIVE FEED
        </span>

        <h2>
          Match Timeline
        </h2>

      </div>

      <div className="timeline">

        {visibleEvents.length === 0 ? (

          <div className="timeline-empty">
            No events available.
          </div>

        ) : (

          visibleEvents.map((event) => (

            <div
              className="event"
              key={event.event_id}
            >

              <div className="event-minute">
                {event.minute}'
              </div>

              <div className="event-marker"></div>

              <div className="event-content">

                <strong>
                  {event.event_type?.replaceAll("_", " ")}
                </strong>

                <span>
                  {event.player} · {event.team}
                </span>

              </div>

            </div>

          ))

        )}

      </div>

    </section>
  );
}


export default Timeline;