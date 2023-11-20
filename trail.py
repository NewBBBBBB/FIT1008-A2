from __future__ import annotations
from dataclasses import dataclass
from data_structures.linked_stack import LinkedStack

from mountain import Mountain

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        next_trail = Trail(None)
        return TrailSeries(self.path_follow.store.mountain, next_trail)


@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""
        return TrailSeries(None, self.following)

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        new_series = TrailSeries(mountain, Trail(TrailSeries(self.mountain, Trail)))
        return new_series

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        return TrailSplit(Trail(None), Trail(None), Trail(self))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        new_following_trail = TrailSeries(mountain, self.following)
        return TrailSeries(self.mountain, Trail(new_following_trail))

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        new_following_trail = TrailSplit(Trail(None), Trail(None), self.following)
        return TrailSeries(self.mountain, Trail(new_following_trail))


TrailStore = Union[TrailSplit, TrailSeries, None]


@dataclass
class Trail:
    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        return Trail(TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        return Trail(TrailSplit(Trail(None), Trail(None), self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality.
        Complexity:
         worst case: O(1), where there is only 1 element inside the stack
         best case: O(n), where n is the number of elements inside the stack
        """

        stack = LinkedStack()
        stack.push(self.store)
        while not stack.is_empty():
            current = stack.pop()
            if isinstance(current, TrailSplit):
                if personality.select_branch(current.path_top, current.path_bottom) is True:
                    if current.path_follow is not None:
                        stack.push(current.path_follow.store)
                    stack.push(current.path_top.store)

                else:
                    if current.path_follow is not None:
                        stack.push(current.path_follow.store)
                    stack.push(current.path_bottom.store)

            elif isinstance(current, TrailSeries):
                personality.add_mountain(current.mountain)
                stack.push(current.following.store)

    def collect_all_mountains(self) -> list[Mountain]:
        """
        Returns a list of all mountains on the trail.
        """
        if self.store is None:
            return []

        stack = [self.store]
        mountains = []

        while stack:
            current_store = stack.pop()

            if isinstance(current_store, TrailSeries):
                mountain = current_store.mountain
                mountains.append(mountain)
                stack.append(current_store.following.store)

            elif isinstance(current_store, TrailSplit):
                if current_store.path_follow is not None:
                    stack.append(current_store.path_follow.store)
                stack.append(current_store.path_top.store)
                stack.append(current_store.path_bottom.store)

        return mountains

    def length_k_paths(self, k: int, path: List[Mountain] = None, stack: LinkedStack = None) -> List[List[Mountain]]:
        """
        Returns all paths of length k through the trail.

        """
        if path is None:
            path = []
        if stack is None:
            stack = LinkedStack()

        paths = []
        trail_store = self.store

        if isinstance(trail_store, TrailSplit):
            new_stack = self.copy_stack(stack)
            new_stack.push(trail_store.path_follow)
            paths += trail_store.path_top.length_k_paths(k, path.copy(), new_stack)

            bottom_stack = self.copy_stack(stack)
            bottom_stack.push(trail_store.path_follow)
            paths += trail_store.path_bottom.length_k_paths(k, path.copy(), bottom_stack)

        elif isinstance(trail_store, TrailSeries):
            path.append(trail_store.mountain)
            paths += trail_store.following.length_k_paths(k, path.copy(), stack)

        elif trail_store is None:
            if len(path) == k:
                paths.append(path)

            if not stack.is_empty():
                follow_trail = stack.pop()
                paths += follow_trail.length_k_paths(k, path.copy(), stack)

        return paths

    def copy_stack(self, stack):
        temp = LinkedStack()
        copy = LinkedStack()
        for _ in range(len(stack)):
            temp.push(stack.pop())
        while not temp.is_empty():
            copy.push(temp.peek())
            stack.push(temp.pop())
        return copy