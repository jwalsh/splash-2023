defmodule Counter do
  @spec server(pid, number) :: atom
  def server(client, total) do
    receive do
      {:incr, value} -> server(client, total + value)
      {:stop} -> terminate(client, total)
    end
  end

  @spec terminate(pid, number) :: atom
  defp terminate(client,total) do
    send(client, {:value, total})
    :ok
  end
end


