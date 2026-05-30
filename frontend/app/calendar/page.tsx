"use client";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { EmptyState } from "@/components/common/empty-state";
import { Calendar, Clock, CheckCircle } from "lucide-react";

const upcomingEvents = [
  {
    title: "Revision Session",
    subject: "Polity",
    time: "Tomorrow, 10:00 AM",
    type: "revision",
  },
  {
    title: "Mock Test",
    subject: "History",
    time: "Day after, 2:00 PM",
    type: "test",
  },
  {
    title: "Study Session",
    subject: "Geography",
    time: "Friday, 9:00 AM",
    type: "study",
  },
];

export default function CalendarPage() {
  const hasEvents = upcomingEvents.length > 0;

  return (
    <div className="p-8">
      <PageHeader
        title="Calendar Overview"
        description="Upcoming study sessions and events"
      />

      {!hasEvents ? (
        <EmptyState
          title="No Upcoming Events"
          description="Add some study sessions to get started"
        />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Calendar className="h-5 w-5" />
                Upcoming Revision Sessions
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {upcomingEvents
                .filter((e) => e.type === "revision")
                .map((event, index) => (
                  <div
                    key={index}
                    className="flex items-start justify-between p-4 rounded-lg border"
                  >
                    <div>
                      <p className="font-medium">{event.title}</p>
                      <p className="text-sm text-muted-foreground">
                        {event.subject}
                      </p>
                    </div>
                    <p className="text-sm text-muted-foreground flex items-center gap-1">
                      <Clock className="h-4 w-4" />
                      {event.time}
                    </p>
                  </div>
                ))}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <CheckCircle className="h-5 w-5" />
                All Upcoming Tasks
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {upcomingEvents.map((event, index) => (
                <div
                  key={index}
                  className="flex items-start justify-between p-4 rounded-lg border"
                >
                  <div>
                    <p className="font-medium">{event.title}</p>
                    <p className="text-sm text-muted-foreground">
                      {event.subject}
                    </p>
                  </div>
                  <p className="text-sm text-muted-foreground flex items-center gap-1">
                    <Clock className="h-4 w-4" />
                    {event.time}
                  </p>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
