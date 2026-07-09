/**
 * Signature visual element — renders course/module completion as a trail of
 * waypoints connected by a dashed path, echoing the "learning PATH" concept
 * instead of a generic progress bar.
 */
export default function WaypointProgress({ steps, currentIndex }) {
  return (
    <div className="flex items-center w-full overflow-x-auto py-2">
      {steps.map((step, i) => (
        <div key={step.id ?? i} className="flex items-center flex-1 min-w-[64px]">
          <div className="flex flex-col items-center gap-1 shrink-0">
            <div
              className={`h-4 w-4 rounded-full border-2 ${
                i < currentIndex
                  ? "bg-trail border-trail"
                  : i === currentIndex
                  ? "bg-waypoint border-waypoint animate-pulse"
                  : "bg-parchment border-mist"
              }`}
              title={step.title}
            />
            <span className="text-[10px] font-mono text-slate max-w-[70px] truncate">{step.title}</span>
          </div>
          {i < steps.length - 1 && (
            <div className={`flex-1 h-0.5 mx-1 ${i < currentIndex ? "bg-trail" : "border-t-2 border-dashed border-mist"}`} />
          )}
        </div>
      ))}
    </div>
  );
}
