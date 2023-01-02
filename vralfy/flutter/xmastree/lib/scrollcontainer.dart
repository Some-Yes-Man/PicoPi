import 'package:flutter/material.dart';
import 'package:sliver_tools/sliver_tools.dart';

class ScrollContainer extends StatelessWidget {
  final Widget? header;
  final Widget? footer;
  final Widget child;

  const ScrollContainer({
    Key? key,
    this.header,
    this.footer,
    required this.child,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    List<Widget> slivers = [];

    if (header != null) {
      slivers.add(
        Card(
          child: Padding(
            padding: EdgeInsets.all(8),
            child: header as Widget,
          ),
        ),
      );
    }

    if (footer != null) {
      slivers.add(
        Card(
          child: Padding(
            padding: EdgeInsets.all(8),
            child: footer as Widget,
          ),
        ),
      );
    }

    return CustomScrollView(
      primary: true,
      slivers: [
        MultiSliver(
          pushPinnedChildren: true,
          children: [
            SliverPinnedHeader(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: slivers,
              ),
            ),
            SliverList(delegate: SliverChildListDelegate([child])),
          ],
        ),
      ],
    );
  }
}
