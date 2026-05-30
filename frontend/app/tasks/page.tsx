"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Plus,
  Edit,
  Trash2,
  CheckCircle,
  Clock,
  Flag,
  Calendar,
  X,
  GripVertical,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PageHeader } from "@/components/common/PageHeader";
import { Skeleton } from "@/components/ui/skeleton";
import { ErrorState } from "@/components/common/error-state";
import { api } from "@/services/api";
import type { Task, TaskCreate, TaskUpdate } from "@/types/dashboard";
import { useToast } from "@/contexts/ToastContext";

const STATUSES = ["pending", "in_progress", "completed"];

export default function TasksPage() {
  const queryClient = useQueryClient();
  const { addToast } = useToast();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [formData, setFormData] = useState<Partial<TaskCreate>>({
    title: "",
    description: "",
    subject: "",
    topic: "",
    priority: "Medium",
    estimated_hours: 1,
    tags: [],
  });

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["tasks"],
    queryFn: async () => {
      const res = await api.tasks.get();
      return res.data.data;
    },
  });

  const createMutation = useMutation({
    mutationFn: (task: TaskCreate) => api.tasks.create(task),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      setIsModalOpen(false);
      resetForm();
      addToast("Task created successfully!", "success");
    },
    onError: (err) => {
      console.error(err);
      addToast("Failed to create task", "error");
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: TaskUpdate }) =>
      api.tasks.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      setIsModalOpen(false);
      setEditingTask(null);
      resetForm();
      addToast("Task updated successfully!", "success");
    },
    onError: (err) => {
      console.error(err);
      addToast("Failed to update task", "error");
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => api.tasks.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      addToast("Task deleted successfully!", "success");
    },
    onError: (err) => {
      console.error(err);
      addToast("Failed to delete task", "error");
    },
  });

  const resetForm = () => {
    setFormData({
      title: "",
      description: "",
      subject: "",
      topic: "",
      priority: "Medium",
      estimated_hours: 1,
      tags: [],
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (editingTask) {
      updateMutation.mutate({
        id: editingTask.id,
        data: formData as TaskUpdate,
      });
    } else {
      createMutation.mutate(formData as TaskCreate);
    }
  };

  const handleEdit = (task: Task) => {
    setEditingTask(task);
    setFormData(task);
    setIsModalOpen(true);
  };

  const handleDelete = (id: string) => {
    if (window.confirm("Are you sure you want to delete this task?")) {
      deleteMutation.mutate(id);
    }
  };

  const handleStatusChange = (task: Task, newStatus: string) => {
    updateMutation.mutate({
      id: task.id,
      data: { status: newStatus },
    });
  };

  const getTasksByStatus = (status: string) => {
    return data?.filter((task) => task.status === status) || [];
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case "high":
        return "text-red-600 bg-red-100";
      case "medium":
        return "text-yellow-600 bg-yellow-100";
      case "low":
        return "text-green-600 bg-green-100";
      default:
        return "text-gray-600 bg-gray-100";
    }
  };

  if (isLoading) {
    return (
      <div className="p-8">
        <PageHeader title="Tasks" description="Manage your tasks" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-96" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <ErrorState
          message="Failed to load tasks"
          onRetry={refetch}
        />
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-8">
        <PageHeader title="Tasks" description="Manage your tasks" />
        <Button onClick={() => {
          resetForm();
          setEditingTask(null);
          setIsModalOpen(true);
        }}>
          <Plus className="h-4 w-4 mr-2" />
          Add Task
        </Button>
      </div>

      {/* Kanban Board */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {STATUSES.map((status) => (
          <div key={status} className="space-y-4">
            <div className="flex items-center gap-2">
              <h3 className="text-lg font-semibold capitalize">
                {status.replace("_", " ")}
              </h3>
              <span className="text-sm text-muted-foreground">
                ({getTasksByStatus(status).length})
              </span>
            </div>
            <div className="space-y-3">
              {getTasksByStatus(status).map((task) => (
                <Card key={task.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-medium flex-1">{task.title}</h4>
                      <div className="flex items-center gap-1">
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-7 w-7"
                          onClick={() => handleEdit(task)}
                        >
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-7 w-7 text-red-600"
                          onClick={() => handleDelete(task.id)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                    {task.description && (
                      <p className="text-sm text-muted-foreground mb-2">
                        {task.description}
                      </p>
                    )}
                    <div className="flex flex-wrap items-center gap-2">
                      <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${getPriorityColor(task.priority)}`}>
                        <Flag className="h-3 w-3 inline mr-1" />
                        {task.priority}
                      </span>
                      <span className="text-xs text-muted-foreground flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {task.estimated_hours}h
                      </span>
                      <span className="text-xs text-muted-foreground flex items-center gap-1">
                        <Calendar className="h-3 w-3" />
                        {task.subject}
                      </span>
                    </div>
                    {task.status !== "completed" && (
                      <div className="mt-3 flex gap-1">
                        {STATUSES.filter(s => s !== status).map((nextStatus) => (
                          <Button
                            key={nextStatus}
                            variant="outline"
                            size="sm"
                            className="text-xs"
                            onClick={() => handleStatusChange(task, nextStatus)}
                          >
                            {nextStatus === "completed" ? (
                              <CheckCircle className="h-3 w-3 mr-1" />
                            ) : (
                              <GripVertical className="h-3 w-3 mr-1" />
                            )}
                            {nextStatus.replace("_", " ")}
                          </Button>
                        ))}
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <Card className="w-full max-w-lg mx-4">
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>
                {editingTask ? "Edit Task" : "Add Task"}
              </CardTitle>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => {
                  setIsModalOpen(false);
                  setEditingTask(null);
                  resetForm();
                }}
              >
                <X className="h-5 w-5" />
              </Button>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Title</label>
                  <Input
                    value={formData.title}
                    onChange={(e) =>
                      setFormData({ ...formData, title: e.target.value })
                    }
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Description</label>
                  <Input
                    value={formData.description}
                    onChange={(e) =>
                      setFormData({ ...formData, description: e.target.value })
                    }
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Subject</label>
                    <Input
                      value={formData.subject}
                      onChange={(e) =>
                        setFormData({ ...formData, subject: e.target.value })
                      }
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Topic</label>
                    <Input
                      value={formData.topic}
                      onChange={(e) =>
                        setFormData({ ...formData, topic: e.target.value })
                      }
                    />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Priority</label>
                    <select
                      value={formData.priority}
                      onChange={(e) =>
                        setFormData({ ...formData, priority: e.target.value })
                      }
                      className="w-full h-10 rounded-md border border-input bg-background px-3 py-2 text-sm"
                    >
                      <option value="High">High</option>
                      <option value="Medium">Medium</option>
                      <option value="Low">Low</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Estimated Hours</label>
                    <Input
                      type="number"
                      value={formData.estimated_hours}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          estimated_hours: parseFloat(e.target.value) || 0,
                        })
                      }
                      min={0.1}
                      step={0.1}
                      required
                    />
                  </div>
                </div>
                <div className="flex justify-end gap-3">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => {
                      setIsModalOpen(false);
                      setEditingTask(null);
                      resetForm();
                    }}
                  >
                    Cancel
                  </Button>
                  <Button type="submit">
                    {editingTask ? "Update" : "Create"}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
